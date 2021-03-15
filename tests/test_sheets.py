"""
Test if dapt.db.sheets.py is working correctly
"""

import os

import dapt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pytest

from tests.base import Database_test_base

conf_path = os.environ['DAPT_config_path']

@pytest.mark.test_creds
class TestGoogleSheets(Database_test_base):
	def preflight(self):
		"""
        Testing items that should be ran before tests are ran.  This method returns a new
        class method for the test.

        Returns:
            The class instance which will be used for the unit test.
        """

		config = dapt.Config(path=conf_path)
		
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		creds = ServiceAccountCredentials.from_json_keyfile_name(config['sheets-creds-path'], scope)

		client = gspread.authorize(creds)
		sheet = client.open_by_key(config.config['sheets-spreedsheet-id'])
		worksheet = sheet.get_worksheet(0)

		data = Database_test_base.INITIAL_TABLE

		start = gspread.utils.rowcol_to_a1(1, 1)
		end = gspread.utils.rowcol_to_a1(len(data)+1, len(data[0])+1)

		range_label = '%s!%s:%s' % (worksheet.title, start, end)

		sheet.values_update(range_label, params={'valueInputOption': 'RAW'}, body={'values': data})

		return dapt.db.Sheet(config=config)

	def test_Sheet_get_key_index(self):
		"""
		Test if the key index function for Sheets works
		"""

		db = self.preflight()

		assert db.get_key_index('a') == 4, "Cannot get the key index."

