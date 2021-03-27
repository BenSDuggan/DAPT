"""

.. _google-sheets:

Google Sheets
=============

Class which allows for Google Sheets to be used as paramater set database.


.. note::

    If you have data in the first row, you must have entries in some other row.

.. _google-sheets-authentication:

Authentication
--------------

TODO

.. _google-sheets-config:

Config
------

The Google Sheets class can be instantiated using a :ref:`config` class.  There are several
options in the config which are redundant (e.g. worksheet-id and worksheet-title).  They are
marked with flags in the table below.  These values should be placed inside a JSON object
named ``google`` or ``google-sheets``.  If the keys are placed inside the ``google`` key,
the values will be shared with other Google APIs (e.g. :ref:`google-drive` ).

+---------------------------+----------------------------------------------------------------+
| Fields                    | Description                                                    |
+===========================+================================================================+
| ``spreedsheet-id`` (str)  | The Google spreedsheet ID being used.  Found in the URL.       |
+---------------------------+----------------------------------------------------------------+
| ``*creds-path`` (str)     | Path to the Google Sheets credentials JSON file.               |
+---------------------------+----------------------------------------------------------------+
| ``*creds`` (dict)         | The Google credentials provided from the developer console.    |
+---------------------------+----------------------------------------------------------------+
| ``#worksheet-id`` (int)   | The Google Sheets worksheet id.  Sheets are indexed at 0.      |
+---------------------------+----------------------------------------------------------------+
| ``#worksheet-title``      |  The Google Sheets worksheet title.                            |
| (str)                     |                                                                |
+---------------------------+----------------------------------------------------------------+

``*`` fields should not be used together.  If you use them together, ``creds`` will be used 
over ``creds-path``.  ``#`` fields should also not be used together and ``worksheet-id`` will
be used.

The default configuration looks like this:

.. code-block:: JSON
    :caption: Sample JSON configuration for ``Sheets``
    :name: example-google-sheets-config

    {
        "google-sheets" : {
            "spreedsheet-id" : "",
            "creds-path" : "",
            "creds" : {},
            "worksheet-id" : "",
            "worksheet-title" : ""
        }
    }


"""

import logging

import gspread
from google.oauth2.service_account import Credentials

from . import base

_log = logging.getLogger(__name__)

class Sheet(base.Database):
    """
    An interface for accessing and setting paramater set data.  You must either provide a Config
    object or client_id and client_secret.

    Keyword Args:
        config (Config): A Config object which contains the client_id and client_secret. 
        spreedsheet_id (str): the Google Sheets ID
         creds (str): the path to the file containing the Google API credentials.  Default is
         ``credentials.json``.
        sheet_id (int): the the sheet id to use.  0 is used if no value is givin for
         sheet_title, sheet_id or in the Config
        sheet_title (str): the title of the sheet to use
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        self.spreedsheetID = None
        self.SCOPE = ['https://www.googleapis.com/auth/spreadsheets',
                      'https://www.googleapis.com/auth/drive']
        self._creds = None
        self.sheet_id = 0
        self.sheet_title = None
        self.config = None

        self.client = None
        self.sheet = None

        if len(kwargs) == 0:
            raise ValueError("Must provide a Config or spreedsheetID and credentials file.")
        if 'config' in kwargs:
            self.config=kwargs['config']

            self._check_old_config()

            self.spreedsheetID = self.config.get_value(
                                    ['google', 'spreedsheet-id'],
                                    recursive=False,
                                    default=self.spreedsheetID)
            self.spreedsheetID = self.config.get_value(
                                    ['google-sheets', 'spreedsheet-id'],
                                    recursive=False,
                                    default=self.spreedsheetID)
            self.sheet_id = self.config.get_value(
                                    ['google', 'worksheet-id'],
                                    recursive=False,
                                    default=self.sheet_id)
            self.sheet_id = self.config.get_value(
                                    ['google-sheets', 'worksheet-id'],
                                    recursive=False,
                                    default=self.sheet_id)
            self.sheet_title = self.config.get_value(
                                    ['google', 'worksheet-title'],
                                    recursive=False,
                                    default=self.sheet_title)
            self.sheet_title = self.config.get_value(
                                    ['google-sheets', 'worksheet-title'],
                                    recursive=False,
                                    default=self.sheet_title)
            if self.config.has_value(['google','creds-path']):
                self._creds = Credentials.from_service_account_file(
                    self.config['google']['creds-path'],
                    scopes=self.SCOPE
                )
            if self.config.has_value(['google-sheets','creds-path']):
                self._creds = Credentials.from_service_account_file(
                    self.config['google-sheets']['creds-path'],
                    scopes=self.SCOPE
                )
            if self.config.has_value(['google', 'creds']):
                self._creds = Credentials.from_service_account_info(
                    self.config['google']['creds'],
                    self.SCOPE
                )
                _log.info('Loaded credentials from Config')
            if self.config.has_value(['google-sheet', 'creds']):
                self._creds = Credentials.from_service_account_info(
                    self.config['google-sheet']['creds'],
                    self.SCOPE
                )
                _log.info('Loaded credentials from Config')

        if 'spreedsheet_id' in kwargs:
            self.spreedsheetID = kwargs['spreedsheet_id']
        if 'creds' in kwargs:
            self._creds = Credentials.from_service_account_file(
                kwargs['creds'],
                scopes=self.SCOPE
            )
        if 'sheet_title' in kwargs:
            self.sheet_title = kwargs['sheet_title']
        if 'sheet_id' in kwargs:
            self.sheet_id = kwargs['sheet_id']
        
        if not self.spreedsheetID:
            raise ValueError("Must specify the spreedsheet id in the arguments or config.")

    def _check_old_config(self):
        """
        Checks the config file to see if Google Sheets is defined using the old method.  If so
        this method will initialize GS using the old mehtod.  The config should already be
        defined and this method will exit if ``self.config`` doesn't have a config set.

        .. deprecated:: 0.9.3
            This method only exists to help phase out the old Google Sheets config.  This
            method will be removed in 0.9.5 when the old config style is removed.
        """

        if self.config is None:
            return
        
        old_method_flag = False

        if self.config.has_value('sheets-spreedsheet-id'):
            old_method_flag = True
            self.spreedsheetID = self.config.config['sheets-spreedsheet-id']
        if self.config.has_value('sheets-creds-path'):
            old_method_flag = True
            self._creds = Credentials.from_service_account_file(
                self.config.config['sheets-creds-path'],
                scopes=self.SCOPE
            )
        if self.config.has_value('sheets-worksheet-id'):
            old_method_flag = True
            self.sheet_id = self.config.config['sheets-worksheet-id']
        if self.config.has_value('sheets-worksheet-title'):
            old_method_flag = True
            self.sheet_title = self.config.config['sheets-worksheet-title']

        if old_method_flag:
            _log.warning('Google Sheet config should be done inside a key named "google" ' \
            'or "google-sheets".  \nSee ' \
            'https://dapt.readthedocs.io/en/latest/reference/db/google_sheets.html#config ' \
            'for more information.')

    def connect(self):
        """
        The method used to connect to the database and log the user in.  Some databases won't
        need to use the connect method, but it should be called regardless to prevent problems.

        Returns:
            gspread client if the database connected successfully and False otherwise.
        """

        # Check the current creds and try to update them
        if self._creds and not self._creds.valid:
            _log.debug('Attempting to update the internal creds')
            self.client = gspread.authorize(self._creds)
        
        self.sheet = self.client.open_by_key(self.spreedsheetID)

        if self.client is None:
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
        Get a Google Sheet object.  The worksheet id or title are obtained from the Config
        file or initialization.

        Returns:
            A Google Sheet worksheet
        """

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
            An array with each element being a dictionary of the key-value pairs for the
            row in the database.
        """

        return self.worksheet().get_all_records()

    def fields(self):
        """
        Get the fields(attributes) of the parameter set
        
        Returns:
            Array of strings with each element being a field (order is preserved if possible)
        """

        return self.worksheet().row_values(1)

    def update_row(self, row_index, values):
        """
        Get the row of the paramater set.

        Args:
            row_index (int): the index of the row to replace (starting from 1).  Indices less
             than 1 will return False.  Indices greater than the table length will be appended.
            values (Dict): the key-value pairs that should be inserted.  If the dictionary
             contains more values then number of columns, the table will be extended.
        
        Returns:
            A boolean that is Trues if successfully inserted and False otherwise.
        """

        if row_index < 0:
            return False

        row = [[]]
        for i in values:
            row[0].append(values[i])
        
        self.connect()

        start = gspread.utils.rowcol_to_a1(row_index+2, 1)
        end = gspread.utils.rowcol_to_a1(row_index+2, len(values))
        range_label = '%s!%s:%s' % (self.worksheet().title, start, end)
        
        return self.sheet.values_update(range_label,
                                        params={'valueInputOption': 'RAW'},
                                        body={'values': row})
        

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

        self.worksheet().update_cell(row_id+2, self.get_key_index(field)+1, str(value))

        return True

    def get_key_index(self, column_key):
        """
        Get the column index given the key.

        Args:
            column_key (str): the key to find the index of
        
        Returns:
            The index or -1 if it could not be determined.
        """

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

        col = self.worksheet().col_values(self.get_key_index(column_key)+1)
        for i in range(len(col)):
            if str(col[i]) == str(row_value):
                return i-1
        return -1
    