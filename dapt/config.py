"""
.. _config:

Config
====== 

The Config class allows user and API settings to be saved and updated using a configuration file.  A config class is not required by DAPT but using one provides several advantages.  First, it makes initializing a class much easier as each class can pull required attributes from a config.  Second, API credentials can be stored in a config, allowing credentials to be kept in one place.  Third, by allowing API tokens to be stored, there is no need to reauthenticate a service (assuming the tokens are still valid).  Finally, it provides a way for users to have their own settings file.

Configuration files `JSON <http://www.json.org>`_ (JavaScript Object Notation) format.  A detailed understanding of JSON is not required, but the basics should be understood.  There are two main components of JSON files: key/value pairs (objects) and arrays/lists.  When using key/value pairs, the pairs must be surrounded by curly braces and seporated with commas.  Objects are seporated by colons (:) and keys must be sourounded by quotes.  Values can be objects, arrays, strings, numbers, booleans, or null.  Bellow is a sample JSON file that could be used by DAPT.

.. _config-example-json:
.. code-block:: JSON
   :caption: Example of a simple JSON file.
   :name: example-json

   {
       "user-name":"Ben",
       "num-of-runs":-1,
       "testing-variables":
       {
           "executable-path":"./main",
           "output-path":"output/"
       }
   }


The ``user-name`` and ``num-of-runs`` keys are reserved DAPT :ref:`fields <config-fields>`.  These cause DAPT to add additional information during tests, initiate classes automatically, and change the testing behavior.  The list of reserved fields and their behaviors are shown bellow.  The ``testing-variables`` key has and object in it that might be used for a specific testing parameters.  They name of this key does not matter as long as it is not a reserved field.  To see how the Config class is used checkout the :ref:`usage <config-usage>` section or class documentation.


.. _config-fields:

Fields
^^^^^^

There are many fields used by modules in DAPT.  A complete list of fields in DAPT is provided below.  These keys are reserved and should not be used in your config file unless you expect DAPT to use them.

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


.. _config-usage:

Usage
^^^^^

For these examples, the :ref:`example JSON <config-example-json>` shown above is used, stored in a file named ``example.json``.  To create a Config object the path to the JSON file must be provided.

.. code-block:: python
   :caption: The Config object is created by providing the path to the JSON object.
   :name: initialize-config

   config = dapt.Config(path="example.json")

The configuration should be accessed using the ``get_value()`` method.  This method will returned the value of the associated key.  Keys can be provided as a string or a list where elements are the path to the value.  The ``num-or-runs`` attribute can be accessed as shown bellow.  

.. code-block:: python
   :caption: The ``num-of-runs`` key should be accessed as shown bellow.
   :name: get-num-of-runs

   config.get_value("num-of-runs")

If you wanted to find the value of ``output-path`` then you specify the path to it.

.. code-block:: python
   :caption: The ``output-path`` key should be accessed as shown bellow.
   :name: get-output-path

   config.get_value(["testing-variables", "output-path"])

Alternatively, the ``output-path`` key can be accessed by using the ``recursive`` flag.  This flag makes the ``get_value()`` method recursively search the JSON tree for the first occupance of the specified key.  This flag will increase the look-up time and may not return the value you expect if multiple keys with that name are present.

The advantage of using the ``get_value()`` method is that ``None`` will be returned if the value is not found.

The configuration dictionary can be accessed indirectly by treating the `Config` object as a dictionary.

.. code-block:: python
   :caption: Accessing ``num-of-runs`` and ``output-path`` from the internal configuration, using the ``Config`` object.
   :name: access-config-indirectly

   config["num-of-runs"]
   config["testing-variables"]["output-path"]

Using this approach, the length of the dictionary can be accessed using Pythons internal `len()` function or any other `dict` method.  The keys of the dictionary can be accessed using the ``Config``s ``keys()`` method.

Before accessing a value in the config, it is good to check that it exists.  This can be done using the `has_value()` method.  This method returns ``True`` if there is a non-none value in the config for the given key.  The key and recursive attributes behave the same as with the ``get_value()`` method.  For example, to check that the ``output-path`` key exists you could run the following and expect a return value of ``True``.

.. code-block:: python
   :caption: Check to see if there is a value for the key ``output-path``.
   :name: has-output-path

   config.has_value(["testing-variables", "output-path"])

If you checked for the key ``foo``, then ``has_value()`` would return ``False``.


Updateing values

Creating default config

Safing config


"""

import json, logging

DEFAULT_CONFIG = {"last-test":None, "user-name":None, "sheets-spreedsheet-id":None, "sheets-creds-path":None, "sheets-worksheet-id":None, "sheets-worksheet-title":None, "num-of-runs":None, "computer-strength":None, "box" : {"client_id" : None, "client_secret" : None, "access_token" : None, "refresh_token" : None, "refresh_time" : None}}

class Config:
    """
    .. _config-docs:

    Config Class Documentation
    ^^^^^^^^^^^^^^^^^^^^^^^^^^

    Class which loads and allows for editing of a config file.

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

    def has_value(self, key, recursive=False):
        """
        Checks to see if the config contains the key and a value other than None.

        Args:
            key (str or list): the key (given as a string) or List containing the path to the value
            recursive (bool): recursively look through the config for the given key.  False by default.  If recursive is set to True then key must be a string.

        Returns:
            True if the key has a value and it's not None, False otherwise.
        """

        if self.get_value(key=key, recursive=recursive) is None:
            return False
        return True

    def keys(self):
        """
        Get the keys from the configuration.  This method only returns the keys at the top of the dictionary.  It will not return any nested keys.

        Returns:
            A list containing the keys in the dictionary.
        """

        return self.config.keys()

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
