"""
    Test if sheets.py is working correctly
"""

import dapt
import os, csv, gspread
from oauth2client.service_account import ServiceAccountCredentials

conf_path = 'test_config.json'

def create_database_entries(config):
	scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name(config.config['sheets-creds-path'], scope)

	client = gspread.authorize(creds)
	sheet = client.open_by_key(config.config['sheets-spreedsheet-id'])
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

	return 

# Test that we can read a delimited file
def test_Sheet_read():
	config = dapt.Config(path=conf_path)
	create_database_entries(config)
	db = dapt.Sheet(config=config)

	expected = [{'id':'t1', 'start-time':'2019-09-06 17:23', 'end-time':'2019-09-06 17:36', 'status':'finished', 'a':2, 'b':4, 'c':6},
				{'id':'t2', 'start-time':'', 'end-time':'', 'status':'', 'a':10, 'b':10, 'c':''},
				{'id':'t3', 'start-time':'', 'end-time':'', 'status':'', 'a':10, 'b':-10, 'c':''}]
	
	actual = db.get_table()

	assert actual == expected, "Cannot read the Google Sheet correctly.  Nothing else should work."

# Test if the keys from a Sheet can be retrieved
def test_Sheet_get_keys():
	config = dapt.Config(path=conf_path)
	db = dapt.Sheet(config=config)
	
	expected = ['id','start-time','end-time','status','a','b','c']

	actual = db.get_keys()

	assert actual == expected, "Cannot get update a row in the Sheet."

# Test if a row in the Sheet can be updated
def test_Sheet_update_row():
	config = dapt.Config(path=conf_path)
	db = dapt.Sheet(config=config)

	expected = [{'id':'t1', 'start-time':'2019-09-06 17:23', 'end-time':'2019-09-06 17:36', 'status':'finished', 'a':2, 'b':4, 'c':6},
				{'id':'t2', 'start-time':'', 'end-time':'', 'status':'', 'a':100, 'b':100, 'c':200},
				{'id':'t3', 'start-time':'', 'end-time':'', 'status':'', 'a':10, 'b':-10, 'c':''}]
	
	db.update_row(1, expected[1])

	assert db.get_table() == expected, "Cannot update a row in the Sheet."

# Test if the row of a Sheet can be updated
def test_Sheet_update_cell():
	config = dapt.Config(path=conf_path)
	db = dapt.Sheet(config=config)
	
	expected = [{'id':'t1', 'start-time':'2019-09-06 17:23', 'end-time':'2019-09-06 17:36', 'status':'finished', 'a':2, 'b':4, 'c':6},
				{'id':'t2', 'start-time':'', 'end-time':'', 'status':'', 'a':100, 'b':100, 'c':200},
				{'id':'t3', 'start-time':'', 'end-time':'', 'status':'', 'a':10, 'b':-10, 'c':0}]
	db.update_cell(2, 'c', expected[2]['c'])

	assert db.get_table() == expected, "Cannot update a cell in the Sheet."

# Test if the key index function for Sheets works
def test_Sheet_get_key_index():
	config = dapt.Config(path=conf_path)
	create_database_entries(config)
	db = dapt.Sheet(config=config)

	assert db.get_key_index('a') == 4, "Cannot get the key index."

# Test if the row index function for Sheets works
def test_Sheet_get_row_index():
	config = dapt.Config(path=conf_path)
	create_database_entries(config)
	db = dapt.Sheet(config=config)

	assert db.get_row_index('id', 't2') == 1, "Cannot get the row index."


