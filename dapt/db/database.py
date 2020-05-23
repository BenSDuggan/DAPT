"""
Database
========

The ``Database`` class is the basic interface for adding parameter set hosting services.  The idea is that the core methods (``get_table``, ``get_keys``, ``update_row`` and ``update_cell``) stay the same so that the inner workings can use multiple sources to access the parameter sets.  You should overide these methods when making a class that inherits ``Database``.  You shouldn't expect that any other method will be called by the ``Param`` class, the main class that uses databases.  It may be benifitial to add helper methods though (e.g. ``get_worksheet()`` in ``Sheets``).  

Databases should give key-value pairs, where the keys are the "ids" of the table and the values are the values in that given row.  When getting the table, the result should be an array of dictionaries that contain the contents of the row.

Indexing
--------

The database should use indexing starting from 0.  

"""

class Database(object):
	"""
	An interface for accessing and setting parameter set data.  
	"""
		
	def __init__(self):

		pass

	def get_table(self):
		"""
		Get the table from the database.

		Returns:
			An array with each element being a dictionary of the key-value pairs for the row in the database.
	    """

		pass

	def get_keys(self):
		"""
		Get the keys of the parameter set
		
		Returns:
			Array of strings with each element being a key (order is preserved if possible)
	    """

		pass

	def update_row(self, row_index, values):
		"""
		Get the keys of the parameter set

		Args:
			row_index (int): the index of the row to replace
			values (Dict): the key-value pairs that should be inserted
		
		Returns:
			A boolean that is True if successfully inserted and False otherwise.
        """

		pass

	def update_cell(self, row_id, key, value):
		"""
		Get the keys of the parameter set

		Args:
			row_id (int): the row id to replace
			key (str): the key of the value to replace
			value (object): the value to insert into the cell
		
		Returns:
			A boolean that is True if successfully inserted and False otherwise.
	    """

		pass
