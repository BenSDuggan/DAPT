"""
.. _base-database:

Base Database
=============

The ``Database`` class is the basic interface for adding parameter set hosting services.  The
idea is that the core methods stay the same so that the inner workings can use multiple sources
to access the parameter sets.  These methods should be overridden when making a class that
inherits ``Database``.  You shouldn't expect that any other method will be called by the
:ref:`param` class, the main class that uses databases.  It may be beneficial to add helper
methods though (e.g. ``get_worksheet()`` in :ref:`google-sheets`).  

Databases should give key-value pairs, where the keys are the "ids" of the table and the values
are the values in that given row.  When getting the table, the result should be an array of
dictionaries that contain the contents of the row.

"""

import logging

_log = logging.getLogger(__name__)

class Database(object):
    """
    An interface for accessing and setting parameter set data.  
    """
        
    def __init__(self):

        pass

    def connect(self):
        """
        The method used to connect to the database and log the user in.  Some databases won't
        need to use the connect method, but it should be called regardless to prevent problems.

        Returns:
            True if the database connected successfully and False otherwise.
        """

        pass

    def connected(self):
        """
        Check to see if the API is connected to the server and working.

        Returns:
            True if the API is connected to the server and False otherwise.
        """

        pass

    def get_table(self):
        """
        Get the table from the database.

        Returns:
            An array with each element being a dictionary of the key-value pairs for the row
            in the database.
        """

        pass

    
    def fields(self):
        """
        Get the fields(attributes) of the parameter set
        
        Returns:
            Array of strings with each element being a field (order is preserved if possible)
        """

        pass

    def get_keys(self):
        """
        .. deprecated:: 0.9.3

        This method is being deprecated in favor of the `fields` method.  It will be removed
        in version 0.9.5.

        Get the keys of the parameter set
        
        Returns:
            Array of strings with each element being a key (order is preserved if possible)
        """

        return self.fields()

    def update_row(self, row_index, values):
        """
        Update the row at the ``row-index`` with the values given.

        Args:
            row_index (int): the index of the row to replace
            values (Dict): the key-value pairs that should be inserted
        
        Returns:
            A boolean that is True if successfully inserted and False otherwise.
        """

        pass

    def update_cell(self, row_id, field, value):
        """
        Update the cell specified by the ``row_id`` and ``field``.

        Args:
            row_id (int): the row id to replace
            field (str): the field of the value to replace
            value (object): the value to insert into the cell
        
        Returns:
            A boolean that is True if successfully inserted and False otherwise.
        """

        pass
