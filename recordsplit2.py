from pymarc import MARCReader
from tkinter import messagebox, filedialog
import re

messagebox.showinfo(title=None,message="Select a batch of records to process")
filename = filedialog.askopenfilename()

file = open(filename,'rb')

reader = MARCReader(file)

nolink = open(f'{str(filename).rstrip('.mrc')}_nolink.mrc','ab')
onelink = open(f'{str(filename).rstrip('.mrc')}_onelink.mrc','ab')
manylink = open(f'{str(filename).rstrip('.mrc')}_manylink.mrc','ab')

URL = re.compile(r'https?://.*')

for record in reader:
    try:
        data = record.get_fields('856')
        count = 0
        for field in data:
            try:
                url = field.get('u')
                if URL.fullmatch(url):
                    count += 1
            except:
                continue
        if count > 1:
            print('Multiple 856 fields found')
            manylink.write(record.as_marc())
        elif count == 1:
            print('Single 856 field found')
            onelink.write(record.as_marc())
        else:
            print('No 856 field found')
            nolink.write(record.as_marc)
    except:
        print('No 856 field found')
        nolink.write(record.as_marc())

print('Process complete. Outputs written to files.')

file.close()
nolink.close()
onelink.close()
manylink.close()