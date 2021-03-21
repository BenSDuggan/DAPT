"""

.. _delimited-file:

Delimited file
==============

This class uses a local `delimited file
<https://en.wikipedia.org/wiki/Delimiter-separated_values>`_ (e.g. CSV, TSV) as a database for
parameter testing.  Delimited files represent a table where the row is a line in the file, and
each column is seporated by a delimiter.  The delimiter is often a comma (comma-seporated file)
or a tab (tab-seporated file).  A CSV file might look like this:

::

    id,start-time,end-time,status,a,b,c
    t1,2019-09-06 17:23,2019-09-06 17:36,finished,2,4,6
    t2,,,,10,10,
    t3,,,,10,-10,

and represent a table that looks like this:

+----+------------------+------------------+----------+----+-----+---+
| id | start-time       | end-time         | status   | a  | b   | c |
+----+------------------+------------------+----------+----+-----+---+
| t1 | 2019-09-06 17:23 | 2019-09-06 17:36 | finished | 2  | 4   | 6 |
+----+------------------+------------------+----------+----+-----+---+
| t2 |                  |                  |          | 10 | 10  |   |
+----+------------------+------------------+----------+----+-----+---+
| t3 |                  |                  |          | 10 | -10 |   |
+----+------------------+------------------+----------+----+-----+---+

Because these files are stored on the users computer, there is no way for a team to work on
the parameter set distributively (without manually dividing the parameter sets up).

Delimited files can have a header which gives the columns names.  The header is the first row
of the table.  Headers must be included with DAPT's ``Delimited_file`` class.

DAPT provides a method named ``sample_db()`` which creates the sample CSV above.  You can create
this file by running that method and then use the ``Delimited_file`` class with it.

    >>> db = dapt.tools.sample_db(file_name='sample_db.csv', delimiter=',')
    >>> db.fields()
    ['id', 'start-time', 'end-time', 'status', 'a', 'b', 'c']


Config
------

Delimited file can accept a :ref:`config` class.  The values listed in the table below are
the same attributes used to instantiate the class.  These values should be placed inside
a JSON object named ``delimited-file.`` 

+---------------------------+----------------------------------------------------------------+
| Fields                    | Description                                                    |
+===========================+================================================================+
| ``path`` (str)            | The path, from the execution directory, to the delimited file. |
+---------------------------+----------------------------------------------------------------+
| ``delimiter`` (str)       | How the columns of the file are seporated.                     |
+---------------------------+----------------------------------------------------------------+

The default configuration looks like this:

.. code-block:: JSON
    :caption: Sample JSON configuration for ``Delimited_file``
    :name: example-delimited-file-config

    {
        "delimited-file" : {
            "path" : "parameters.csv", 
            "delimiter" : ","
        }
    }

"""

import csv
import logging
import os

from . import base

_log = logging.getLogger(__name__)

class Delimited_file(base.Database):
    """
    An interface for accessing and setting paramater set data.  

    Keyword args:
        path (str): path to delimited file file
        delimiter (str): the delimiter of the CSV.  ``,`` by default.
        config (``Config`` object): an Config instance
    """
        
    def __init__(self, *args, **kwargs):
        
        super().__init__()
        
        self.config = None
        self.path = None
        self.delimiter = ','

        if len(kwargs) == 0 and len(args) == 0:
            raise ValueError("You must provide a Config object or path to the CSV.")
        if 'config' in kwargs:
            self.config = kwargs['config']
            if self.config.has_value('delimited-file'):
                if self.config.has_value(['delimited-file', 'path']):
                    self.path = self.config['delimited-file']['path']
                if self.config.has_value(['delimited-file', 'delimiter']):
                    self.delimiter = self.config['delimited-file']['delimiter']
        
        # Check for values given as args
        if len(args) > 0:
            self.path = args[0]
            if len(args) > 1:
                self.delimiter = args[1]

        # Check for values given as kwargs
        if 'path' in kwargs:
            self.path = kwargs['path']
        if 'delimiter' in kwargs:
            self.delimiter = kwargs['delimiter']


    def connect(self):
        """
        The method used to connect to the database and log the user in.  Some databases won't
        need to use the connect method, but it should be called regardless to prevent problems.

        Returns:
            True if the database connected successfully and False otherwise.
        """

        return self.connected()

    def connected(self):
        """
        Check to see if the API is connected to the server and working.

        Returns:
            True if the API is connected to the server and False otherwise.
        """

        if os.path.exists(self.path) and os.path.isfile(self.path):
            try:
                with open(self.path, 'r') as csvfile:
                    csv.DictReader(csvfile, delimiter=self.delimiter)
                
            except Exception as e:
                _log.warning("Cannot read the delimited file: %s" % str(e))
                return False
            
            if not os.access(self.path, os.W_OK):
                _log.warning("Cannot write to delimited file.")
                return False
                
            return True
        else:
            _log.warning("Delimited file does not exist.")

        return False

    def get_table(self):
        """
        Get the table from the database.

        Returns:
            An array with each element being a dictionary of the key-value pairs for the row
            in the database.
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
            or ``None`` if the file is empty.
        """

        with open(self.path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)

            return next(reader, None)

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

