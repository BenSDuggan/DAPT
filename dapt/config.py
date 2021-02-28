"""
.. _config:

Config
======

The Config class allows user and API settings to be saved and updated using a configuration file.
A config class is not required by DAPT but using one provides several advantages.  First, it
makes initializing a class much easier as each class can pull required attributes from a config.
Second, API credentials can be stored in a config, allowing credentials to be kept in one place.
Third, by allowing API tokens to be stored, there is no need to reauthenticate a service (assuming
the tokens are still valid).  Finally, it provides a way for users to have their own settings
file.

Configuration files use `JSON <http://www.json.org>`_ (JavaScript Object Notation) format.  A
detailed understanding of JSON is not required, but the basics should be understood.  There are
two main components of JSON files: key/value pairs (objects) and arrays/lists.  When using
key/value pairs, the pairs must be surrounded by curly braces and seporated with commas.  Objects
are seporated by colons (:) and keys must be sourounded by quotes.  Values can be objects, arrays,
strings, numbers, booleans, or null.  Bellow is a sample JSON file that could be used by DAPT.

.. _config-example-json:

.. code-block:: JSON
   :caption: Example of a simple JSON file.
   :name: example-json

   {
       "performed-by":"Ben",
       "num-of-runs":-1,
       "testing-variables":
       {
           "executable-path":"./main",
           "output-path":"output/"
       }
   }


The ``performed-by`` and ``num-of-runs`` keys are reserved DAPT :ref:`fields <config-fields>`.
These cause DAPT to add additional information during tests, initiate classes automatically,
and change the testing behavior.  The list of reserved fields and their behaviors are shown
bellow.  The ``testing-variables`` key has and object in it that might be used for a specific
testing parameters.  They name of this key does not matter as long as it is not a reserved field.
To see how the Config class is used checkout the :ref:`usage <config-usage>` section or class
documentation.

.. _config-fields:

Fields
^^^^^^

There are many key-value pairs which can be used in the configuration to make DAPT behave in a
particular way.  These keys are called fields.  These fields are reserved and should not be used
in your config file unless you expect DAPT to use them.  A list of top level fields is provided
below.  

+---------------------------+----------------------------------------------------------------+
| Fields                    | Description                                                    |
+===========================+================================================================+
| ``num-of-runs`` (int)     | The number of paramater sets to run.                           |
+---------------------------+----------------------------------------------------------------+
| ``performed-by`` (str)    | The username of the person that ran the parameter set.         |
+---------------------------+----------------------------------------------------------------+
| ``last-test`` (str)       | The last test id that was run.  If a test exits before         |
|                           | completeing, it will be re-ran.                                |
+---------------------------+----------------------------------------------------------------+
| ``computer-strength``     | Only run tests on computers with sufficient power.  The        |
| (int)                     | parameter set will only be run if this value is greater than   |
|                           | or equal that of the parameter sets ``computer-strength``.     |
+---------------------------+----------------------------------------------------------------+
| ``sheets-spreedsheet-id`` | The Google spreedsheet ID being used.                          |
| (str)                     |                                                                |
+---------------------------+----------------------------------------------------------------+
| ``sheets-creds-path``     | The Google Sheets credentials file path.                       |
| (str)                     |                                                                |
+---------------------------+----------------------------------------------------------------+
| ``sheets-worksheet-id``   | The Google Sheets worksheet id.  Sheets are indexed at 0.      |
| (str)                     |                                                                |
+---------------------------+----------------------------------------------------------------+
| ``sheets-worksheet-title``| The Google Sheets worksheet title.                             |
| (str)                     |                                                                |
+---------------------------+----------------------------------------------------------------+
| ``box`` (str)             | Values used by the :ref:`box` storage API.                     |
+---------------------------+----------------------------------------------------------------+
| ``reset-time`` (str)      | The time that the box access-token needs to be refreshed.      |
+---------------------------+----------------------------------------------------------------+

Some of these fields are used by other DAPT classes to store values.  For example, the
``google-sheets`` field has many sub-fields that set parameters in the class automatically.
The ``spreedsheet-id`` sub-field sets the spreedsheet ID that should be used as the database.
These sub-fields are not listed above.  They are notable, however, because you may accidentally
find one of these sub-fields if you recursively search a config file.  If you are worried about
accidentally using one of these fields, the ``FULL_CONFIG`` variable in the
`config <https://github.com/BenSDuggan/DAPT/blob/master/dapt/config.py>`__ module contains all
of the config fields.

.. _config-usage:

Usage
^^^^^

For these examples, the :ref:`example JSON <config-example-json>` shown above is used, stored in a
file named ``example.json``.  To create a Config object the path to the JSON file must be 
provided.

    >>> config = dapt.Config(path="example.json")

The configuration should be accessed using the ``get_value()`` method.  This method will returned
the value of the associated key.  Keys can be provided as a string or a list where elements are
the path to the value.  The ``num-or-runs`` attribute can be accessed as shown bellow.

    >>> config.get_value("num-of-runs")
    -1

If you wanted to find the value of ``output-path`` then you specify the path to it.

    >>> config.get_value(["testing-variables", "output-path"])
    'output/'

Alternatively, the ``output-path`` key can be accessed by using the ``recursive`` flag.  This
flag makes the ``get_value()`` method recursively search the JSON tree for the first occupance
of the specified key.  This flag will increase the look-up time and may not return the value you
expect if multiple keys with that name are present.

The advantage of using the ``get_value()`` method is that ``None`` will be returned if the value
is not found.

The configuration dictionary can be accessed indirectly by treating the `Config` object as a
dictionary.

    >>> config["num-of-runs"]
    -1
    >>> config["testing-variables"]["output-path"]
    'output/'

Using this approach, the length of the dictionary can be accessed using Pythons internal `len()`
function or any other `dict` method.  The keys of the dictionary can be accessed using the
``keys()`` method.

Before accessing a value in the config, it is good to check that it exists.  This can be done
using the ``has_value()`` method.  This method returns ``True`` if there is a non-none value in
the config for the given key.  The key and recursive attributes behave the same as with the
``get_value()`` method.  For example, to check that the ``output-path`` key exists you could
run the following and expect a return value of ``True``.::

    >>> config.has_value(["testing-variables", "output-path"])
    True

If you checked for the key ``foo``, then ``has_value()`` would return ``False``.

To add key-value pairs to the configuration or update values, the ``update()`` method should
be used.  This method will allow the configuration to change and save it to the JSON file.
The configuration can be changed in four different ways.  First, by providing the key as a string.
Second, by providing the key as an array representing a path to the value.  The third method
uses a ``str`` for the string and recursively finds the first occurrence of the key in the config.
Lastly, the configuration can be updated by accessing the dictionary directly.  Then ``update()``
can be ran without parameters to save the config.  The second and last methods are required to
access nested key-value pairs.  All of these methods work to add new data or change values in
the configuration.

    >>> config.update(key="performed-by", value="John", recursive=False)
    {'performed-by': 'John', 'num-of-runs': -1, 
     'testing-variables': {'executable-path': './main', 'output-path': 'output/'}}
    >>> config.update(key=["testing-variables", "executable-path"], value="main.exe",
                      recursive=False)
    {'performed-by': 'John', 'num-of-runs': -1,
     'testing-variables': {'executable-path': 'main.exe', 'output-path': 'output/'}}
    >>> config.update(key="output-path", value="save/", recursive=True)
    {'performed-by': 'John', 'num-of-runs': -1,
     'testing-variables':{'executable-path': 'main.exe', 'output-path': 'save/'}}

    >>> config["num-of-runs"] = 3
    >>> config.update()
    {'performed-by': 'John', 'num-of-runs': 3,
     'testing-variables':{'executable-path': 'main.exe', 'output-path': 'save/'}}

When creating a new configuration file, the ``create()`` method can be used.  This static method
will create a default configuration file at the path provided.  This file contains all of the
possible fields used by DAPT.

    >>> dapt.config.Config.create(path="new-config.json")

Configuration files can contain sensitive API credentials or passwords.  Storing these in plane
text or publishing configuration files online is unsecure as people can then gain access to your
online services.  To combate this you can "safe" the configuration file.  The ``safe()`` method
will remove all API credentials from the configuration so the file cannot be used to access your
APIs.  Currently, this this process is one-way and the credentials cannot be recovered.
However, in the future this will encrypt the file can be distributed online and unlocked by people
with the correct password.


"""

import json, logging

_log = logging.getLogger(__name__)

DEFAULT_CONFIG = {"last-test":None, "performed-by":None, "num-of-runs":None, 
                  "computer-strength":None, "sheets-spreedsheet-id":None,
                  "sheets-creds-path":None, "sheets-worksheet-id":None, 
                  "sheets-worksheet-title":None, 
                  "box" : {"client_id" : None, "client_secret" : None, "access_token" : None,
                           "refresh_token" : None, "refresh_time" : None}}
FULL_CONFIG = DEFAULT_CONFIG

class Config:
    """
    .. _config-docs:

    Class which loads and allows for editing of a config file.

    Args:
        path (string): path to config file
    """
    def __init__(self, path='config.json'):
        self.path = path
        self.config = self.read()

    def get_value(self, key, recursive=False):
        """
        Get the first value of the given key or return ``None`` if one doesn't exist.

        Args:
            key (str or list): the key (given as a string) or List containing the path to the
             value
            recursive (bool): recursively look through the config for the given key.  False by
             default.  If recursive is set to True then key must be a string.

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

    def _find_path(self, dic, key):
        """
        Helper function to find the path to a nested key

        Args:
            dic (dict): the dictionary
            key (str): the key to search for

        Returns:
            An `arr` containing the path to the key in the dic or None if the path could not be
             found
        """

        if key in dic:
            return [key]
        
        for k, v in dic.items():
            if isinstance(v, dict):
                keys = self._find_path(v, key)
                if keys:
                    return [k] + keys
        return None

    
    def read(self):
        """
        Reads the file with path set to self.path

        Returns:
            Dictionary of config file
        """

        with open(self.path) as f:
            self.config = json.load(f)
            return self.config

    def update(self, key=None, value=None, recursive=False):
        """
        Given a key and associated value, updated the config file.  Alternatively, you can give
        no arguments and the config dict will be saved.  You can also do both.

        Args:
            key (str or list): the key (given as a string) or List containing the path to the
             value.  If `None` is given then nothing will be updated in the dictionary.
            value (str): the value associated ot the key.
            recursive (bool): recursively look through the config for the given key.  False by
             default.  If recursive is set to True then key must be a string.

        Returns:
            Dictionary of config file
        """

        if key:
            if recursive:
                path = self._find_path(self.config, key)

                # If the path has not been found then the key is likely not in the dict yet
                if path:
                    key = path

            # Convert key to list if it is not already one
            if not isinstance(key, list):
                key = [key]
            
            dic = self.config

            for k in key:
                if k == key[-1]:
                    dic[k] = value
                elif k in dic:
                    dic = dic[k]
                else:
                    dic[k] = {}
                    dic = dic[k]
        
        with open(self.path, 'w') as f:
            json.dump(self.config, f)

        return self.config

    def has_value(self, key, recursive=False):
        """
        Checks to see if the config contains the key and a value other than None.

        Args:
            key (str or list): the key (given as a string) or List containing the path to the
             value
            recursive (bool): recursively look through the config for the given key.  False by
             default.  If recursive is set to True then key must be a string.

        Returns:
            True if the key has a value and it's not None, False otherwise.
        """

        if self.get_value(key=key, recursive=recursive) is None:
            return False
        return True

    def keys(self):
        """
        Get the keys from the configuration.  This method only returns the keys at the top of
        the dictionary.  It will not return any nested keys.

        Returns:
            A list containing the keys in the dictionary.
        """

        return self.config.keys()

    @staticmethod
    def create(path='config.json'):
        """
        Creates a config file with the reserved keys inserted.  The ``DEFAULT_CONFIG`` will
        be used.

        Args:
            path (string): path where config file will be written

        Returns:
            A ``Config`` object with the newly created default configuration
        """
        
        with open(path, 'w') as f:
            json.dump(DEFAULT_CONFIG, f)

        return Config(path)

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
        
        conf.update()

    def __len__(self):
        return len(self.config)

    def __getitem__(self, key):
        return self.config[key]
    
    def __setitem__(self, key, value):
        self.update(key, value)

    def __delitem__(self, key):
        del self.config[key]

    def __repr__(self):
        return repr(self.config)

    def __iter__(self):
        return iter(self.config)

    def __contains__(self, item):
        return item in self.config
