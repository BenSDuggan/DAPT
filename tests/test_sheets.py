"""
    Test if sheets.py is working correctly
"""

import dapt
import os, csv
from collections import OrderedDict 

conf_path = 'test_config.json'

def create_database_entries(config):
	sheet = dapt.Sheet(config=config)
	
	# Reset the sheet
	test_worksheet = None
	worksheets = sheet.sheet.worksheets()
	for i in worksheets:
		if i.title == 'daptTest':
			test_worksheet = i
			break
	
	if test_worksheet:
		sheet.sheet.del_worksheet(test_worksheet)

	# Create a new worksheet
	sheet.sheet.add_worksheet(title="daptTest", rows="3", cols="3")

	header = ['id', 'a', 'c']
	data = [{'id':'t1', 'a':'2', 'c':'4'}]
	#data = [{'id':'t1', 'a':'2', 'c':'4'}, {'id':'t2', 'a':'10', 'c':''}]

	for i in range(len(header)):
		sheet.worksheet(title='daptTest').update_cell(1, i+1, header[i])
		for j in range(len(data)):
			sheet.worksheet(title='daptTest').update_cell(j+2, i+1, data[j][header[i]])

# Test that we can read a delimited file
def test_Sheet_read():
	config = dapt.Config(path=conf_path)

	create_database_entries(config)

	db = dapt.Sheet(config=config)
	
	actual = db.get_table()

	expected = []
	expected.append({'id':'t1', 'a':2, 'c':4})
	#expected.append({'id':'t2', 'a':10, 'c':''})

	assert actual == expected, "Cannot read the Google Sheet correctly.  Nothing else should work."

# Test if the keys from a Sheet can be retrieved
def test_Sheet_get_keys():
	config = dapt.Config(path=conf_path)

	create_database_entries(config)

	db = dapt.Sheet(config=config)
	
	actual = db.get_keys()

	expected = ['id', 'a', 'c']

	assert actual == expected, "Cannot get update a row in the Sheet."

# Test if a cell in the Sheet can be updated
def test_Sheet_update_row():
	config = dapt.Config(path=conf_path)

	create_database_entries(config)

	db = dapt.Sheet(config=config)
	
	db.update_row(1, {'id':'t1', 'a':2, 'c':20})
	
	expected = []
	expected.append({'id':'t1', 'a':2, 'c':20})
	#expected.append({'id':'t2', 'a':10, 'c':20})

	assert db.get_table() == expected, "Cannot update a row in the Sheet."

# Test if the row of a Sheet can be updated
def test_Sheet_update_cell():
	config = dapt.Config(path=conf_path)

	create_database_entries(config)

	db = dapt.Sheet(config=config)
	
	db.update_cell(1, 'c', 30)
	
	expected = []
	expected.append({'id':'t1', 'a':2, 'c':30})
	#expected.append({'id':'t2', 'a':10, 'c':20})

	assert db.get_table() == expected, "Cannot update a cell in the Sheet."

# Test if the key index function for Sheets works
def test_Sheet_get_key_index():
	config = dapt.Config(path=conf_path)

	create_database_entries(config)

	db = dapt.Sheet(config=config)

	assert db.get_key_index('c') == 2, "Cannot get the key index."

# Test if the row index function for Sheets works
def test_Sheet_get_row_index():
	config = dapt.Config(path=conf_path)

	create_database_entries(config)

	db = dapt.Sheet(config=config)

	assert db.get_row_index('c', 4) == 1, "Cannot get the row index."


