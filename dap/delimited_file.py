"""
    Delimited file
    ==============

    Create a CSV instance which can be used by param to get and run param sets
"""

import csv, os
from . import database

class Delimited_file(database.Database):
    def __init__(self, csv_file, delimiter=','):
        """
            An interface for accessing and setting paramater set data.  
        """
        super().__init__()

        self.csv_file = csv_file
        self.delimiter = delimiter

    def get_table(self):
        """
            Get the table from the database.

            Returns:
                An array with each element being a dictionary of the key-value pairs for the row in the database.
        """

        sheet = []
        with open(self.csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter)
            for row in reader:
                sheet.append(row)
        return sheet

    def get_keys(self):
        """
            Get the keys of the paramater set
            
            Returns:
                Array of strings with each element being a key (order is preserved if possible)
        """

        with open(self.csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            return next(reader)

    def update_row(self, row_id, values):
        """
            Get the keys of the paramater set

            Args:
                row_id (int): the row id to replace
                values (OrderedDict): the key-value pairs that should be inserted
            
            Returns:
                A boolean that is True if successfully inserted and False otherwise.
        """

        header = self.get_keys()
        table = self.get_table()

        with open(self.csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()

            table[row_id] = values

            for row in table:
                writer.writerow(row)

            return True

    def update_cell(self, row_id, key, value):
        """
            Get the keys of the paramater set

            Args:
                row_id (int): the row id to replace
                key (str): the key of the value to replace
                value (str): the value to insert into the cell
            
            Returns:
                A boolean that is True if successfully inserted and False otherwise.
        """

        header = self.get_keys()
        table = self.get_table()

        with open(self.csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()

            table[row_id][key] = value

            for row in table:
                writer.writerow(row)

            return True 

if __name__ == '__main__':
    print('CSV sheet:')
    c = Delimited_file('../examples/test.csv', ',')
    print("get_keys: " + str(c.get_keys()))
    print("get_table: " + str(c.get_table()))
    print("update_cell: " + str(c.update_cell(1, "endTime", "09/02/19 12:10:00")))
    print("get_table: " + str(c.get_table()))
    print("update_row: " + str(c.update_row(1, {"id":"st-2", "startTime":"09/01/19 22:05:00", "endTime":""})))
    print("get_table: " + str(c.get_table()))