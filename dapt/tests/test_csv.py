# Test that config is working properly

import dap
import os

# Test creation of new config file
def test_config_create():
	dap.csv.CSV('dapt/tests/test.csv', ',')
	
	conf = dap.config.Config.readConfig('dapt/tests/config.txt')
	expected = {"lastTest":None, "userName":None, "spreedsheetID":None, "client_id":None, "client_secret":None, "boxFolderID":None, "resetTime":None, "numOfRuns":None, "computerStrength":None, "accessToken":None, "refressToken":None}

	os.remove('dapt/tests/config.txt')

	assert conf == expected, "The Config.create() method that creates a new and empty config file returned wrong."
