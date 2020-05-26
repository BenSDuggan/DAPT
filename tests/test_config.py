"""
    Test if config.py is working correctly
"""

import dapt
import os

# Test creation of new config file
def test_config_create():
	dapt.Config.create('config.json')

	conf = dapt.Config('config.json')
	expected = {"last-test":None, "user-name":None, "sheets-spreedsheet-id":None, "sheets-creds-path":None, "sheets-worksheet-id":None, "sheets-worksheet-title":None, "client-id":None, "client-secret":None, "box-folder-id":None, "reset-time":None, "num-of-runs":None, "computer-strength":None, "access-token":None, "refresh-token":None}

	os.remove('config.json')

	assert conf.config == expected, "The Config.create() method that creates a new and empty config file returned wrong."

# Test changing a value in Config
def test_config_file_change():
	dapt.Config.create('config.json')

	conf = dapt.Config('config.json')

	expected = conf.config
	expected["user-name"] = 'Clifford'

	conf.config["user-name"] = 'Clifford'
	conf.update_config()

	os.remove('config.json')

	assert conf.config == expected, "Config did not change the value correctly."

# Test adding a key,value pair in Config
def test_config_file_add():
	dapt.Config.create('config.json')

	conf = dapt.Config('config.json')

	expected = conf.config
	expected["abc"] = 123

	conf.config["abc"] = 123
	conf.update_config()

	os.remove('config.json')

	assert conf.config == expected, "Config did not add the key,value pair correctly."

# Test adding a key,value pair in Config
def test_config_get_value_str():
	dapt.Config.create('config.json')

	conf = dapt.Config('config.json')

	conf.config["abc"] = 123
	conf.update_config()

	os.remove('config.json')

	assert conf.get_value("abc") == 123, "Config.get_value(\"abc\",recursive=False): Config did not find the correct value."

def test_config_get_value_arr():
	dapt.Config.create('config.json')

	conf = dapt.Config('config.json')

	conf.config["abc"] = {"a":1, "b":2, "c":{"aa":11, "bb":22}}
	conf.update_config()

	os.remove('config.json')

	assert conf.get_value(["abc", "c", "aa"]) == 11, 'Config.get_value(["abc", "c", "aa"],recursive=False): Config did not find the correct value.'

def test_config_get_value_recursive():
	dapt.Config.create('config.json')

	conf = dapt.Config('config.json')

	conf.config["abc"] = {"a":1, "b":2, "c":{"aa":11, "bb":22}}
	conf.update_config()

	os.remove('config.json')

	assert conf.get_value("aa", recursive=True) == 11, 'Config.get_value("aa",recursive=True): Config did not find the correct value.'

# Test making config file safe for uploading publicly
def test_config_safe():
	dapt.Config.create('config.json')
	conf = dapt.Config('config.json')

	expected = conf.config
	expected["access-token"] = ''
	expected["refresh-token"] = ''

	dapt.Config.safe('config.json')

	os.remove('config.json')

	assert conf.config == expected, "Conf did not make the config file safe."

# Test the has_value method when the key is not in the config
def test_config_has_value_null():
	dapt.Config.create('config.json')

	conf = dapt.Config('config.json')

	os.remove('config.json')

	assert conf.has_value('fried-chicken') == False, "Config.has_value() should return False when key is not in the config"

# Test the has_value method when the key has a value of None
def test_config_has_value_None():
	dapt.Config.create('config.json')

	conf = dapt.Config('config.json')

	os.remove('config.json')

	assert conf.has_value('last-test') == False, "Config.has_value() should return False when key has a value of None"

# Test the has_value method when the key has a value
def test_config_has_value_positive():
	dapt.Config.create('config.json')

	conf = dapt.Config('config.json')
	conf.update_config(key='last-test', value='3a')

	os.remove('config.json')

	assert conf.has_value('last-test') == True, "Config.has_value() should return True when key has a value"

# Test the Config __dict__ method
def test_config_dict():
	dapt.Config.create('config.json')

	config = dapt.Config('config.json')
	
	os.remove('config.json')

	assert config.config == config.__dict__(), "The Config.__dict__() method doesn't return the internal config"