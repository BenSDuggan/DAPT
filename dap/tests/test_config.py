# Test that config is working properly

import dap
import os

# Test creation of new config file
def test_config_create():
	dap.config.Config.create('dap/tests/config.txt')

	conf = dap.config.Config.readConfig('dap/tests/config.txt')
	expected = {"lastTest":None, "userName":None, "spreedsheetID":None, "client_id":None, "client_secret":None, "boxFolderID":None, "resetTime":None, "numOfRuns":None, "computerStrength":None, "accessToken":None, "refressToken":None}

	os.remove('dap/tests/config.txt')

	assert conf == expected, "The Config.create() method that creates a new and empty config file returned wrong."

# Test parsing of Config
def test_config_file_parseing():

	with open('dap/tests/config.txt', 'w') as f:
		f.writelines('test_int:123\ntest_float:300.1\ntest_None:None\ntest_char:a\ntest_bool:False\ntest_string:hi')

	conf = dap.config.Config.readConfig('dap/tests/config.txt')
	expected = {"test_int":123, "test_float":300.1, "test_None":None, "test_char":'a', "test_bool":False, "test_string":'hi'}

	os.remove('dap/tests/config.txt')

	assert conf == expected, "The Config file parser did not work."

# Test changing a value in Config
def test_config_file_change():
	dap.config.Config.create('dap/tests/config.txt')

	conf = dap.config.Config('dap/tests/config.txt')

	expected = conf.config
	expected["userName"] = 'Clifford'

	conf.change_config('userName', 'Clifford')

	os.remove('dap/tests/config.txt')

	assert conf.config == expected, "Config did not change the value correctly."

# Test adding a key,value pair in Config
def test_config_file_add():
	dap.config.Config.create('dap/tests/config.txt')

	conf = dap.config.Config('dap/tests/config.txt')

	expected = conf.config
	expected["dog_type"] = 'Bloodhound'

	conf.change_config('dog_type', 'Bloodhound')

	os.remove('dap/tests/config.txt')

	assert conf.config == expected, "Config did not add the key,value pair correctly."

# Test making config file safe for uploading publicly
def test_config_safe():
	dap.config.Config.create('dap/tests/config.txt')
	conf = dap.config.Config('dap/tests/config.txt')

	expected = conf.config
	expected["accessToken"] = ''

	conf.safe('dap/tests/config.txt')

	os.remove('dap/tests/config.txt')

	assert conf.config == expected, "Conf did not make the config file safe."
