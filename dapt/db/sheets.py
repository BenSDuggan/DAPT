"""

.. _google-sheets:

Google Sheets
=============

Class which allows for Google Sheets to be used as paramater set database.


Note: if you have data in the first row, you must have entries in some other row.
"""

import logging

import gspread
from google.oauth2.service_account import Credentials

from . import base

_log = logging.getLogger(__name__)

class Sheet(base.Database):
    """
    An interface for accessing and setting paramater set data.  You must either provide a Config object or client_id and client_secret.

    Keyword Args:
        config (Config): A Config object which contains the client_id and client_secret. 
        spreedsheet_id (str): the Google Sheets ID
        creds (str): the path to the file containing the Google API credentials.  Default is ``credentials.json``.
        sheet_id (int): the the sheet id to use.  0 is used if no value is givin for sheet_title, sheet_id or in the Config
        sheet_title (str): the title of the sheet to use
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        self.spreedsheetID = None
        #self.SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.SCOPE = ['https://www.googleapis.com/auth/spreadsheets',
                      'https://www.googleapis.com/auth/drive']
        self._creds = None
        self.sheet_id = -1
        self.sheet_title = None
        self.config = None

        self.client = None
        self.sheet = None

        if len(kwargs) == 0:
            raise ValueError("You must provide a Config object or spreedsheetID and credentials file.")
        if 'config' in kwargs:
            self.config=kwargs['config']

            if self.config.has_value('sheets-spreedsheet-id'):
                self.spreedsheetID = self.config.config['sheets-spreedsheet-id']
            if self.config.has_value('sheets-creds-path'):
                self._creds = Credentials.from_service_account_file(
                    self.config.config['sheets-creds-path'],
                    scopes=self.SCOPE
                )
            if self.config.has_value('sheets-worksheet-id'):
                self.sheet_id = self.config.config['sheets-worksheet-id']
            if self.config.has_value('sheets-worksheet-title'):
                self.sheet_title = self.config.config['sheets-worksheet-title']
        if not self.spreedsheetID:
            if 'spreedsheet_id' in kwargs:
                self.spreedsheetID = kwargs['spreedsheet_id']
            else:
                raise ValueError("You must specify the spreedsheet id in the arguments or config.")
        if not self._creds:
            if 'creds' in kwargs:
                self._creds = Credentials.from_service_account_file(
                    kwargs['creds'],
                    scopes=self.SCOPE
                )
            else:
                self._creds = Credentials.from_service_account_file(
                    self.config.config['sheets-creds-path'],
                    scopes=self.SCOPE
                )
        if not self.sheet_title and self.sheet_id == -1:
            if 'sheet_title' in kwargs:
                self.sheet_title = kwargs['sheet_title']
        if self.sheet_id == -1 and not self.sheet_title:
            if 'sheet_id' in kwargs:
                self.sheet_id = kwargs['sheet_id']
            else:
                self.sheet_id = 0

    def connect(self):
        """
        The method used to connect to the database and log the user in.  Some databases won't
        need to use the connect method, but it should be called regardless to prevent problems.

        Returns:
            Gspread client if the database connected successfully and False otherwise.
        """

        # Check the current creds and try to update them
        if self._creds and not self._creds.valid:
            _log.debug('Attempting to update the internal creds')
            self.client = gspread.authorize(self._creds)

        self.sheet = self.client.open_by_key(self.spreedsheetID)

        if not self.connected():
            return False
        
        return self.client

    def connected(self):
        """
        Check to see if the API is connected to the server and working.

        Returns:
            True if the API is connected to the server and False otherwise.
        """

        try:
            # True to get the first value of the first sheet
            c = self.sheet.sheet1.get('A1')
            return True
        except Exception as e:
            _log.warning('Cannot connect to Google Sheets: %s' % str(e))
            return False

    def worksheet(self, *args, **kwargs):
        """
        Get a Google Sheet object.  The worksheet id or title are obtained from the Config file or initialization.

        Returns:
            A Google Sheet worksheet
        """

        self.connect()

        if self.sheet_title:
            return self.sheet.worksheet(self.sheet_title)
        elif self.sheet_id >= 0:
            return self.sheet.get_worksheet(self.sheet_id)
        else:
            return self.sheet.get_worksheet(0)

    def get_table(self):
        """
        Get the table from the database.

        Returns:
            An array with each element being a dictionary of the key-value pairs for the row in the database.
        """

        self.connect()

        return self.worksheet().get_all_records()

    def fields(self):
        """
        Get the fields(attributes) of the parameter set
        
        Returns:
            Array of strings with each element being a field (order is preserved if possible)
        """

        self.connect()

        return self.worksheet().row_values(1)

    def update_row(self, row_index, values):
        """
        Get the row of the paramater set.

        Args:
            row_index (int): the index of the row to replace (starting from 1).  Indices less than 1 will return False.  Indices greater than the table length will be appended.
            values (Dict): the key-value pairs that should be inserted.  If the dictionary contains more values then number of columns, the table will be extended.
        
        Returns:
            A boolean that is Trues if successfully inserted and False otherwise.
        """

        self.connect()

        if row_index < 0:
            return False

        row = [[]]
        for i in values:
            row[0].append(values[i])
        
        self.connect()

        start = gspread.utils.rowcol_to_a1(row_index+2, 1)
        end = gspread.utils.rowcol_to_a1(row_index+2, len(values))
        range_label = '%s!%s:%s' % (self.worksheet().title, start, end)
        
        try:
            return self.sheet.values_update(range_label, params={'valueInputOption': 'RAW'}, body={'values': row})
        except:
            return False
        return True

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
        try:
            self.connect()
            self.worksheet().update_cell(row_id+2, self.get_key_index(field)+1, str(value))
        except Exception as e:
            raise e
        return True

    def get_key_index(self, column_key):
        """
        Get the column index given the key.

        Args:
            column_key (str): the key to find the index of
        
        Returns:
            The index or -1 if it could not be determined.
        """

        self.connect()

        key_map = {}
        key_row = self.worksheet().row_values(1)
        for i in range(len(key_row)):
            if str(key_row[i]) == str(column_key):
                return i
        return -1

    def get_row_index(self, column_key, row_value):
        """
        Get the row index given the column to look through and row value to match to.

        Args:
            column_key (str): the key to find the index of
            row_value (str): the value of the cell to fine
        
        Returns:
            The index or -1 if it could not be determined.
        """

        self.connect()

        col = self.worksheet().col_values(self.get_key_index(column_key)+1)
        for i in range(len(col)):
            if str(col[i]) == str(row_value):
                return i-1
        return -1
    