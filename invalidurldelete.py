from pymarc import MARCReader, Record
import pandas as pd
from tkinter import messagebox, filedialog
import datetime

#Define function for collecting urls
def collect_urls(urllist):
    duds = []
    df = pd.read_csv(urllist)
    for index, row in df.iterrows():
        print(f'Invalid url: {row['URL']}')
        duds.append(str(row['URL']).strip().lower().rstrip('/'))
    #Troubleshooting
    count = 0
    for i in duds:
        count += 1
        with open('formatcheck_duds.txt','a',encoding='utf-8') as fl:
            fl.write(f'{repr(i)}\n')
    print(f'{count} broken urls found.')
    input('Press enter to continue...')
    return duds

#Define function for checking 856$u
def check_856u(field, duds):
    url = str(field.get('u')).strip().lower().rstrip('/')
    with open('formatcheck_records.txt','a', encoding='utf-8') as fl:
        fl.write(f'{repr(url)}\n')
    if url in duds:
        print(f'{url} found in broken links list')
        with open('errorlogging.txt','a', encoding='utf-8') as fk:
            fk.write(f'{url} found in broken links list\n')
        return True
    else:
        print(f'{url} is valid!')
        with open('errorlogging.txt','a') as fk:
            fk.write(f'{url} is valid!\n')
        return False

def main():
    #Prompt for list of broken links (output from marclinkcheck)
    messagebox.showinfo(title=None, message="Please select a file with invalid URLs to delete (.csv file from marclinkcheck.py).")
    urllist = filedialog.askopenfilename()
    #Prompt for records to process
    messagebox.showinfo(title=None, message="Please select a set of MARC records to process in .mrc format.")
    records = filedialog.askopenfilename()
    #Collect list of dud records
    print('Collecting list of dud links...')
    duds = collect_urls(urllist)
    #Create timestamp for output
    timestamp = datetime.datetime.now().strftime('%m%d%H%M')
    #Check 856u for each record against duds list and write output
    print('Checking records for broken links...')
    with open(records, 'rb') as fh:
        reader = MARCReader(fh)
        count = 0
        for record in reader:
            fields = record.get_fields('856')
            delete = []
            for field in fields:
                url = field.get('u')
                if url != None:
                    print(url)
                    status = check_856u(field, duds)
                    if status == True:
                        delete.append(field)
                else:
                    print('No URL found in field.')
                    count += 1
                    print(f'{count} 856 fields w/o $u')
            for field in delete:
                record.remove_field(field)
            with open(f'validurls{timestamp}.mrc','ab') as fj:
                fj.write(record.as_marc())
    print(f'Invalid URLs removed and output written to validurls{timestamp}.mrc.')

if __name__ == "__main__":
    main()