'''
    Ben Duggan
    1/8/19
    Main script to run distributed parameter testing
'''

import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Sheet:
    def __init__(self, spreedsheetID, creds_path="credentials.json"):
        self.spreedsheetID = spreedsheetID
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, self.scope)

    # use creds to create a client to interact with the Google Drive API
    def sheet(self, sheet_id=0):
        client = gspread.authorize(creds)

        return client.open_by_key(spreedsheetID).get_worksheet(sheet_id)

    def getRecords(self):
        return sheet().get_all_records()

    def update_cell(self, i, j, text):
        self.sheet().update_cell(i+2, j, text)