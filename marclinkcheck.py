from tkinter import filedialog, messagebox
import re
import datetime
import socket
from pymarc import MARCReader
import requests
import time

HTTP = re.compile('^https?://.*')
BROKEN = 'PID,URL,Status\n'

def domaincheck(url, valid_domains, invalid_domains):
    domain = re.sub(r'^https?://([^/]+).*',r'\1',url)
    if domain in valid_domains:
        return True
    elif domain in invalid_domains:
        return False
    else:
        try:
            socket.gethostbyname(domain)
            print(f'Host {domain} is valid.')
            valid_domains.append(domain)
            return True
        except Exception as e:
            print(f'Host {domain} is invalid. Exception: {e}')
            invalid_domains.append(domain)
            return False

def collecturls(reader):
    global BROKEN
    urls = []
    print('Collecting URLs...')
    valid_domains = []
    invalid_domains = []
    for record in reader:
        record_id = str(record['001']).lstrip('=001  ')
        linking = record.get_fields('856')
        for field in linking:
            try:
                url = str(field.get('u')).strip()
                if HTTP.match(url):
                    valid = domaincheck(url, valid_domains, invalid_domains)
                    if valid == True:
                        print(record_id, url)
                        urls.append((record_id,url))
                    else:
                        BROKEN = BROKEN + '\"' + record_id + '\",\"' + url + '\",\"Invalid domain\"\n'
                else:
                    print(f'Invalid URL: {url}')
            except Exception as e:
                print(f'Error: {e} for record {record_id}')
                urls.append((record_id,None))
    print('URLs collected. Beginning status checks...')
    return urls

def statuscheck(record_id, url):
    if url != None:
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code == 200:
                print(url, response.status_code)
                return (record_id, url, response.status_code)
            elif response.status_code == 403 or response.status_code == 405:
                print('HEAD request denied. Sending GET...')
                response2 = requests.get(url, allow_redirects=True)
                if response2.status_code == 200:
                    print(url, response2.status_code)
                    return (record_id, url, response2.status_code)
                elif response2.status_code == 429:
                    status = retry(url)
                    return (record_id, url, status)
                else:
                    print(url, response2.status_code)
                    return (record_id, url, response2.status_code)
            elif response.status_code == 429:
                status = retry(url)
                return (record_id, url, status)  
            else:
                print(url, response.status_code)
                return (record_id, url, response.status_code)
        except Exception as e:
            print(f'Error {e} for {url} from {record_id}')
            return (record_id, url, str(e))
    else:
        return (record_id, 'None', 'No valid URL')

def retry(url):
    for i in range(7):
        print(f'Request blocked. Waiting {2**i} seconds...')
        time.sleep(2**i)
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            return response.status_code
        elif response.status_code == 429:
            continue
        else:
            return response.status_code
    return '429 (Block and Timeout)'

def main():
    global BROKEN
    messagebox.showinfo(title=None, message='Select a .mrc file to check for valid URLs')
    file = filedialog.askopenfilename()
    file = open(file, 'rb')
    reader = MARCReader(file)
    urls = collecturls(reader)
    for record_id, url in urls:
        status = statuscheck(record_id, url)
        if status[2] != 200:
            BROKEN = BROKEN + '\"' + status[0] + '\"' + ',' + '\"' + status[1] + '\"' + ',' + '\"' + str(status[2]) + '\"' + '\n'
    timestamp = datetime.datetime.today().strftime('%m%d%H%M')
    with open(f'brokenlinks{timestamp}.csv','w', encoding='utf-8') as fh:
        fh.write(BROKEN)
    print(f'Process completed successfully. Broken links saved to brokenlinks{timestamp}.csv.')

if __name__ == "__main__":
    main()