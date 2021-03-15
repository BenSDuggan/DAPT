"""
Base classes for testing.  These classes make it easy to add tests for a new database or storage
class.  Each test class that inherits a testing class must implement the ``preflight()`` method.
This method sets up the testing environment and resets it from past tests.  The 
``postflight()`` method cleans up after the test.  Class specific tests can also be created.
"""

class Database_test_base:
    INITIAL_TABLE = [['id','start-time','end-time','status','a','b','c'],
                    ['t1','2019-09-06 17:23','2019-09-06 17:36','finished','2','4','6'],
                    ['t2','','','','10','10',''],
                    ['t3','','','','10','-10','']]
    INITIAL_DICT = [{'id':'t1', 'start-time':'2019-09-06 17:23', 'end-time':'2019-09-06 17:36', 'status':'finished', 'a':'2', 'b':'4', 'c':'6'},
				{'id':'t2', 'start-time':'', 'end-time':'', 'status':'', 'a':'10', 'b':'10', 'c':''},
				{'id':'t3', 'start-time':'', 'end-time':'', 'status':'', 'a':'10', 'b':'-10', 'c':''}]

    def preflight(self):
        """
        Testing items that should be ran before tests are ran.  This method returns a new
        class method for the test.

        Returns:
            The class instance which will be used for the unit test.
        """

        pass

    def postflight(self):
        """
        Clean up after tests are ran.
        """

        pass

    def test_read_table(self):
        """
        Test that we can read a delimited file
        """

        db = self.preflight()
        
        actual = db.get_table()

        # Cast values to string (problem with GS type inferencing)
        actual = [{str(k):str(v) for k,v in r.items()} for r in actual] 

        expected = Database_test_base.INITIAL_DICT

        assert actual == expected, "Cannot read the table.  Nothing else should work."

        self.postflight()

    
    def test_DF_get_fields(self):
        """
        Test if the keys from a delimited file can be retrieved
        """

        db = self.preflight()
        
        actual = db.fields()
        expected = ['id', 'start-time', 'end-time', 'status', 'a', 'b', 'c']

        assert actual == expected, "Cannot get update a row in the delimited file."

        self.postflight()

    def test_update_row(self):
        """
        Test if a cell in the delimited file can be updated
        """
        
        db = self.preflight()

        db.update_row(1, {'id':'t2', 'start-time':'2019-09-06 17:37', 'end-time':'2019-09-06 17:55', 'status':'finished', 'a':'10', 'b':'10', 'c':'20'})
        
        expected = [{'id':'t1', 'start-time':'2019-09-06 17:23', 'end-time':'2019-09-06 17:36', 'status':'finished', 'a':'2', 'b':'4', 'c':'6'},
				{'id':'t2', 'start-time':'2019-09-06 17:37', 'end-time':'2019-09-06 17:55', 'status':'finished', 'a':'10', 'b':'10', 'c':'20'},
				{'id':'t3', 'start-time':'', 'end-time':'', 'status':'', 'a':'10', 'b':'-10', 'c':''}]
            
        actual = db.get_table()

        # Cast values to string (problem with GS type inferencing)
        actual = [{str(k):str(v) for k,v in r.items()} for r in actual] 

        assert actual == expected, "Cannot update a row in the delimited file."

        self.postflight()
    
    def test_update_cell(self):
        """
        Test if the row of a delimited file can be updated
        """

        db = self.preflight()
        
        db.update_cell(1, 'status', 'adding')
        
        expected = [{'id':'t1', 'start-time':'2019-09-06 17:23', 'end-time':'2019-09-06 17:36', 'status':'finished', 'a':'2', 'b':'4', 'c':'6'},
				{'id':'t2', 'start-time':'', 'end-time':'', 'status':'adding', 'a':'10', 'b':'10', 'c':''},
				{'id':'t3', 'start-time':'', 'end-time':'', 'status':'', 'a':'10', 'b':'-10', 'c':''}]
        
        actual = db.get_table()

        # Cast values to string (problem with GS type inferencing)
        actual = [{str(k):str(v) for k,v in r.items()} for r in actual] 

        assert actual == expected, "Cannot update a cell in the delimited file."

        self.postflight()
    
    def test_DF_get_row_index(self):
        """
        Test if the row of a delimited file can be updated
        """
        
        db = self.preflight()

        assert db.get_row_index('status', 'finished') == 0, "Cannot get the row index."

        self.postflight()