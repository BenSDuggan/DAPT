"""
Config
====== 

Class that allows for reading and modification of a configuration (config) file.  A config file is not required but using one will make using DAPT much easier to use and greatly increase increase it's functionality.  A configuration file is simply a JSON file.  There are some reserved keys but you can add your own and refer to them throughout your program.


Fields
^^^^^^

There are several standard fields (keys) that are used by DAPT for credentials and parameter settings.

+----------------------------------+-----------------------------------------------------------------------------------------+
| Fields                           | Description                                                                             |
+==================================+=========================================================================================+
| ``last-test`` (str)              | The last test id that was run.                                                          |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``user-name`` (str)              | The box username of the user.                                                           |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``sheets-spreedsheet-id`` (str)  | The Google spreedsheet ID being used.                                                   |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``sheets-creds-path`` (str)      | The Google Sheets credentials file path.                                                |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``sheets-worksheet-id`` (str)    | The Google Sheets worksheet id.  Sheets are indexed at 0.                               |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``sheets-worksheet-title`` (str) | The Google Sheets worksheet title.                                                      |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``client-id`` (str)              | Box API client ID.                                                                      |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``client-secret`` (str)          | Box API client secret.                                                                  |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``box-folder-id`` (str)          | The box folder id to use                                                                |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``reset-time`` (str)             | The time that the box access-token needs to be refreshed.                               |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``num-of-runs`` (int)            | The number of paramater sets to run.                                                    |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``computer-strength`` (int)      | Any comments such as error messages relating to the parameter set.                      |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``access-token`` (str)           | The box access token for the particular session.                                        |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``refresh-token`` (str)          | The box refresh token for the particular session.                                       |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``remove-zip`` (bool)            | Have tools.data_cleanup() remove zip files if true.                                     |
+----------------------------------+-----------------------------------------------------------------------------------------+
| ``remove-movie`` (bool)          | Have tools.data_cleanup() remove mp4 files if true.                                     |
+----------------------------------+-----------------------------------------------------------------------------------------+

Usage
^^^^^

The Config class can be used like a normal dictionary.

"""

import json

DEFAULT_CONFIG = {"last-test":None, "user-name":None, "sheets-spreedsheet-id":None, "sheets-creds-path":None, "sheets-worksheet-id":None, "sheets-worksheet-title":None, "num-of-runs":None, "computer-strength":None, "box" : {"client_id" : None, "client_secret" : None, "access_token" : None, "refresh_token" : None, "refresh_time" : None}}

class Config:
    """
    Class which loads and allows for editing of a config file

    Args:
        path (string): path to config file
    """
    def __init__(self, path='config.json'):
        self.path = path
        self.config = self.read_config()

    def get_value(self, key, recursive=False):
        """
        Get the first value of the given key or return ``None`` if one doesn't exist.

        Args:
            key (str or list): the key (given as a string) or List containing the path to the value
            recursive (bool): recursively look through the config for the given key.  False by default.  If recursive is set to True then key must be a string.

        Returns:
            The value associated to the given key or None if the key is not in the dictionary.
        """

        # If we we want to do it recursively
        if recursive:
            return self._find_value(self.config, key)
        
        value = None

        # Convert key to list if it is not already one
        if not isinstance(key, list):
            key = [key]

        if key[0] in self.config:
            value = self.config[key[0]]

            for i in range(1, len(key)):
                if key[i] in value:
                    value = value[key[i]]
                else:
                    return None
        
        return value

    def _find_value(self, dic, key):
        """
        Helper function to find value recursively

        Args:
            dic (dict): the dictionary
            key (str): the key to search for

        Returns:
            The object associated to the given key or None if not found.
        """

        if key in dic:
            return dic[key]
        
        for k, v in dic.items():
            if isinstance(v, dict):
                value = self._find_value(v, key)
                if value:
                    return value
        return None

    
    def read_config(self):
        """
        Reads the file with path set to self.path

        Returns:
            Dictionary of config file
        """

        with open(self.path) as f:
            return json.load(f)

    def update_config(self, key=None, value=None):
        """
        Given a key and associated value, updated the config file.  Alternatively, you can give no arguments and the config dict will be saved.  You can also do both.

        Args:
            key (str): the key to use.  If none is given then nothing will be updated in the dictionary.
            value (str): the value associated ot the key.

        Returns:
            Dictionary of config file
        """

        if key:
            self.config[key] = value

        with open(self.path, 'w') as f:
            json.dump(self.config, f)

        return self.config

    def has_value(self, key):
        """
        Checks to see if the config contains the key and a value other than None.

        Args:
            key (str): The key to determine if it has a value

        Returns:
            True if the key has a value, False otherwise.
        """

        if self.get_value(key, recursive=True) is None:
            return False
        return True

    @staticmethod
    def create(path='config.json'):
        """
        Creates a config file with the reserved keys inserted.

        Args:
            path (string): path where config file will be written
        """
        
        with open(path, 'w') as f:
            json.dump(DEFAULT_CONFIG, f)

    @staticmethod
    def safe(path="config.json"):
        """
        Safe config file by removing accessToken and refreshToken.

        Args:
            path (string): path where config file will be writen
        """
        conf = Config(path)

        if conf.has_value(("box", "access-token")):
            conf["box"]["access-token"] = None
        if conf.has_value(("box", "refresh-token")):
            conf["box"]["refresh-token"] = None
        
        conf.update_config()

    def __len__(self):
        return len(self.config)

    def keys(self):
        return self.config.keys()

    def __getitem__(self, key):
        return self.config[key]
    
    def __setitem__(self, key, value):
        self.update_config(key, value)

    def __delitem__(self, key):
        del self.config[key]

    def __repr__(self):
        return repr(self.config)

    def __iter__(self):
        return iter(self.config)

    def __contains(self, item):
        return item in self.config
