"""

.. _delimited-file:

Delimited file
==============

Create a CSV database which can be used by param to get and run param sets.  
"""

import csv
import logging
import os

from . import base

_log = logging.getLogger(__name__)

class Delimited_file(base.Database):
    """
    An interface for accessing and setting paramater set data.  

    Args:
        path (string): path to delimited file file
    """
        
    def __init__(self, path, delimiter=','):
        
        super().__init__()
        
        self.path = path
        self.delimiter = delimiter

    def connect(self):
        """
        This method isn't required for Delimeted files as there is nothing to connect to.
        It will return True regardless.

        Returns:
            True if the database connected successfully and False otherwise.
        """

        return True

    def get_table(self):
        """
        Get the table from the database.

        Returns:
            An array with each element being a dictionary of the key-value pairs for the row in the database.
        """

        sheet = []
        with open(self.path, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter)
            for row in reader:
                sheet.append(row)
        return sheet

    def fields(self):
        """
        Get the fields(attributes) of the parameter set
        
        Returns:
            Array of strings with each element being a field (order is preserved if possible)
        """

        with open(self.path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            return next(reader)

    def update_row(self, row_index, values):
        """
        Update the row at the ``row-index`` with the values given.

        Args:
            row_index (int): the index of the row to replace
            values (Dict): the key-value pairs that should be inserted
        
        Returns:
            A boolean that is True if successfully inserted and False otherwise.
        """

        header = self.fields()
        table = self.get_table()

        with open(self.path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()

            table[row_index] = values

            for row in table:
                writer.writerow(row)

            return True

    def update_cell(self, row_index, field, value):
        """
        Update the cell specified by the ``row_id`` and ``field``.

        Args:
            row_id (int): the row id to replace
            field (str): the field of the value to replace
            value (object): the value to insert into the cell
        
        Returns:
            A boolean that is True if successfully inserted and False otherwise.
        """

        header = self.fields()
        table = self.get_table()

        with open(self.path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()

            table[row_index][field] = value

            for row in table:
                writer.writerow(row)

            return True 
            
    def get_row_index(self, column_key, row_value):
        """
        Get the row index given the column to look through and row value to match to.

        Args:
            column_key (str): the column to use.
            row_value (str): the row value to match with in the file and determin the row index.
        
        Returns:
            The index or -1 if it could not be determined
        """

        table = self.get_table()

        index = 0
        for row in table:
            if row[column_key] == row_value:
                return index
            index += 1

        return -1

