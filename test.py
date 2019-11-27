# Test sheet many row update

import dapt, gspread
from oauth2client.service_account import ServiceAccountCredentials

config = dapt.Config(path='test_config.json')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(config.config['sheets-creds-path'], scope)

client = gspread.authorize(creds)
sheet = client.open_by_key(config.config['spreedsheet-id'])
worksheet = sheet.get_worksheet(0)

config = dapt.Config(path='test_config.json')
sheet = dapt.Sheet(config=config)

data = [['id','start-time','end-time','status','a','b','c'],
        ['t1','2019-09-06 17:23','2019-09-06 17:36','finished','2','4','6'],
        ['t2','','','','10','10',''],
        ['t3','','','','10','-10','']]

start = gspread.utils.rowcol_to_a1(1, 1)
end = gspread.utils.rowcol_to_a1(len(data)+1, len(data[0])+1)

range_label = '%s!%s:%s' % (worksheet.title, start, end)

sheet.sheet.values_update(range_label, params={'valueInputOption': 'RAW'}, body={'values': data})

exit()

title = 'tests'

# Data to upload
data = [['hellow', 'world']]

# Get coords
coords = (1, 1, 2, 1) # start row, end row.  By col then row
start = gspread.utils.rowcol_to_a1(coords[0], coords[1])
end = gspread.utils.rowcol_to_a1(coords[2], coords[3])

range_label = '%s!%s:%s' % (title, start, end)

# Update

data = sheet.sheet.values_update(
            range_label,
            params={
                'valueInputOption': 'RAW'
            },
            body={
                'values': data
            }
        )

print(data)

# Check

