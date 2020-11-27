"""
    Test if param.py is working correctly.  
    
    There should be tests for when users only include the required fields and also when they give any optional ones.  Additionally, there needs to be tests for when a Config file is used and for when one is not.
"""

import dapt
import os, csv, datetime
from collections import OrderedDict 

# Create a test file with just the required fields
def create_simple_test_file():
	with open('test.csv', 'w') as f:
		writer = csv.DictWriter(f, fieldnames=['id', 'status', 'a', 'b', 'c'])
		writer.writeheader()
		writer.writerow({'id':'t1', 'status':'successful', 'a':'2', 'b':'4', 'c':'6'})
		writer.writerow({'id':'t2', 'status':'', 'a':'10', 'b':'10', 'c':''})
		writer.writerow({'id':'t3', 'status':'', 'a':'10', 'b':'-10', 'c':''})

# Create a test file that has all the possible fields
def create_complex_test_file():
	with open('test.csv', 'w') as f:
		writer = csv.DictWriter(f, fieldnames=['id', 'start-time', 'end-time', 'status', 'comment','performed-by', 'a', 'b', 'c'])
		writer.writeheader()
		writer.writerow({'id':'t1', 'start-time':'2019-09-06 17:23', 'end-time':'2019-09-06 17:36', 'status':'successful', 'comment':'2+4=6','performed-by':'ben', 'a':'2', 'b':'4', 'c':'6'})
		writer.writerow({'id':'t2', 'start-time':'', 'end-time':'', 'status':'', 'comment':'','performed-by':'', 'a':'10', 'b':'10', 'c':''})
		writer.writerow({'id':'t3', 'start-time':'', 'end-time':'', 'status':'', 'comment':'','performed-by':'', 'a':'10', 'b':'-10', 'c':''})


# Test that the next paramater set can be retrived
def test_Param_next_parameters():
	create_simple_test_file()

	db = dapt.Delimited_file('test.csv', ',')

	param = dapt.Param(db)	
	actual = param.next_parameters()

	expected = OrderedDict({'id':'t2', 'status':'in progress', 'a':'10', 'b':'10', 'c':''})
    
	assert actual == expected, "Cannot get the next paramater set."

# Test if the status can be updated
def test_Param_update_status():
    create_simple_test_file()

    db = dapt.Delimited_file('test.csv', ',')

    param = dapt.Param(db)
    actual = param.next_parameters()
    actual = param.update_status(actual['id'], 'adding')

    expected = OrderedDict({'id':'t2', 'status':'adding', 'a':'10', 'b':'10', 'c':''})

    assert actual == expected, "Cannot update the status of the paramater set."

# Test if failed works
def test_Param_successful():
    create_simple_test_file()

    db = dapt.Delimited_file('test.csv', ',')

    param = dapt.Param(db)
    actual = param.next_parameters()
    actual = param.successful(actual['id'])

    expected = OrderedDict({'id':'t2', 'status':'successful', 'a':'10', 'b':'10', 'c':''})

    assert actual == expected, "Cannot update the status of the paramater set."

# Test if failed with optional fields
def test_Param_successful_fields():
    create_complex_test_file()

    db = dapt.Delimited_file('test.csv', ',')

    param = dapt.Param(db)
    actual = param.next_parameters()
    expected = actual
    actual = param.successful(actual['id'])
    
    expected = OrderedDict({'id':'t2', 'start-time':'', 'end-time':'', 'status':'successful', 'comment':'','performed-by':'', 'a':'10', 'b':'10', 'c':''})

    # Check to see if the time in the database are within 15 seconds of ours.
    if (datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(actual['start-time'], '%Y-%m-%d %H:%M:%S')).seconds < 15:
        expected['start-time'] = actual['start-time']
    if (datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(actual['end-time'], '%Y-%m-%d %H:%M:%S')).seconds < 15:
        expected['end-time'] = actual['end-time']
    
    assert actual == expected, "Cannot update the status of the paramater set."

# Test if failed works
def test_Param_failed():
    create_simple_test_file()

    db = dapt.Delimited_file('test.csv', ',')

    param = dapt.Param(db)
    actual = param.next_parameters()
    actual = param.failed(actual['id'], 'This is an error')

    expected = OrderedDict({'id':'t2', 'status':'failed', 'a':'10', 'b':'10', 'c':''})

    assert actual == expected, "Cannot update the status of the paramater set."

# Test if failed with optional fields
def test_Param_failed_fields():
    create_complex_test_file()

    db = dapt.Delimited_file('test.csv', ',')

    param = dapt.Param(db)
    actual = param.next_parameters()
    expected = actual
    actual = param.failed(actual['id'], 'This is an error')

    expected = OrderedDict({'id':'t2', 'start-time':'', 'end-time':'', 'status':'failed', 'comment':'','performed-by':'', 'a':'10', 'b':'10', 'c':''})

    # Check to see if the time in the database are within 15 seconds of ours.
    if (datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(actual['start-time'], '%Y-%m-%d %H:%M:%S')).seconds < 15:
        expected['start-time'] = actual['start-time']
    if (datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(actual['end-time'], '%Y-%m-%d %H:%M:%S')).seconds < 15:
        expected['end-time'] = actual['end-time']
    
    assert actual == expected, "Cannot update the status of the paramater set."
