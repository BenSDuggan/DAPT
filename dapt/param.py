"""
.. _param:
Parameters
==========

This is the main class which interact with the database to get and manage parameter sets.  The ``Param`` class links all the other classes together enabling a paramater set to be run.

.. _param-database:
Database
--------

In order to get the paramaters, the ``Param`` class needs to be given a ``Database`` instance (e.g. ``Sheets``, ``Delimited_file``).  The database is where the parameters to be tested live.  The database has a couple required fields (attributes) and many optional fields.  The param-fields_ section provides more information on how the database should be configured.

Each time a new parameter set is requested, the database will be downloaded again.  This means that the database can be changed as DAPT is running to add or remove the number of tests.  An important note regarding database is that they can be ran local or on the internet.  This means that multiple people can work on the parameter set at the same time, thus distributing the computational work load.

.. _param-database-fields:
Fields
^^^^^^

A field is the key (or identifier) used to get the value when a parameter set is returned.  Each database is required to have and ``id`` and ``status`` field.  There are many optional fields which can be used to give additionally information about the run such as start time and who performed the run.  Below are the fields that are used with parsing parameter sets.  Required parameters are marked with an astrict(*).

+---------------------------+-----------------------------------------------------------------------------------------+
| Fields                    | Description                                                                             |
+===========================+=========================================================================================+
| ``id``\* (str)            | Unique parameter set installed                                                          |
+---------------------------+-----------------------------------------------------------------------------------------+
| ``status``\* (str)        | The current status of the parameter set. Blank values(default) have not been ran,       |
|                           | ``successful`` have finished and ``failed`` have failed.                                |
+---------------------------+-----------------------------------------------------------------------------------------+
| ``start-time`` (str)      | The time that the parameter set began.  Times are in UTC time format.                   |
+---------------------------+-----------------------------------------------------------------------------------------+
| ``end-time`` (str)        | The time that the parameter set finished.  Times are in UTC time format.                |
+---------------------------+-----------------------------------------------------------------------------------------+
| ``performed-by`` (str)    | The username of the person that ran the parameter set.                                  |
+---------------------------+-----------------------------------------------------------------------------------------+
| ``comments`` (str)        | Any comments such as error messages relating to the parameter set.                      |
+---------------------------+-----------------------------------------------------------------------------------------+

The ``id`` field is a unique identifier for that test.  This attribute is used to identify the parameter set and must be given to most of the methods in the ``Param`` class.  The ``status`` filed gives the current status of the test.  There are five main status values: empty, "successful", "failed", "in progress", and other text.  When a test has an empty status it indicates that the test has not been ran yet.  A status of "successful" indicates that the test has finished successfully, and a "failed" status shows that the test failed.  When you request another parameter set by running ``next_parameters()``, the status will automatically be set to "in progress".  If the status is not empty, then DAPT will not offer it when the ``next_parameters()`` method is called.  You can update the status to something you want by calling the ``update_status()`` method.

.. _param-usage:
Usage
-----

"""

import datetime, logging

_log = logging.getLogger(__name__)

class Param:
    """
    Create a Param instance with a database and optional config file.

    Args:
        database (Database): a Database instance (such as Sheets or Delimited_file)
        config (Config): a config object which allows for more features.  This is optional.
    """
    

    def __init__(self, database, config=None):
        self.db = database
        self.performed_by = ''
        self.number_of_runs = -1
        self.runs_performed = 0
        self.computer_strength = float('inf')

        self.config = config
        if self.config:
            if self.config.has_value('num-of-runs'):
                self.number_of_runs = self.config.config['num-of-runs']
            if self.config.has_value('performed-by'):
                self.performed_by = self.config.config['performed-by']
            if self.config.has_value('computer-strength'):
                self.computer_strength = self.config.config['computer-strength']

    def next_parameters(self):
        """
        Get the next parameter set if one exists
        
        Returns:
            An OrderedDict containing the key-value pairs from that parameter set or None if there are no more to sets.
        """

        if self.number_of_runs == -1 or self.runs_performed < self.number_of_runs:
            self.runs_performed += 1
            _log.debug('%d runs performed (calls to `next_parameters()`)' % self.runs_performed)
        else:
            _log.info('No more parameters to test in the database.')
            return None
        
        records = self.db.get_table()
        _log.debug('Retrieved %d parameters' % len(records))

        # Do we have a last-test in the config file
        if self.config and "last-test" in self.config and self.config["last-test"]:
            _log.info('Using `last-test` with id="%s" from config.txt' % str(self.config["last-test"]))
            for i in range(0, len(records)):
                if str(self.config.config["last-test"]) == str(records[i]["id"]) and records[i]["status"] != "successful":
                    records[i]["status"] = "in progress"
                    if "start-time" in records[i]:
                        records[i]["start-time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if "performed-by" in records[i]:
                        records[i]["performed-by"] = self.performed_by

                    self.db.update_row(i, records[i])

                    return records[i]

        for i in range(0, len(records)):
            if not len(records[i]["status"]):
                if 'computer-strength' in records[i] and self.computer_strength < int(records[i]["computer-strength"]):
                    continue
                
                records[i]["status"] = "in progress"
                if "start-time" in records[i]:
                    records[i]["start-time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if "performed-by" in records[i]:
                    records[i]["performed-by"] = self.performed_by
                self.db.update_row(i, records[i])

                # Save id to local cache
                if self.config:
                    self.config.update(key='last-test', value=str(records[i]["id"]))

                return records[i]

        return None

    def update_status(self, id, status):
        """
        Update the status of the selected parameter.  If status is not included in the parameter set keys then nothing will be updated.

        Args:
            id (str): the id of the parameter set to use
        
        Returns:
            The new parameter set that has been updated or False if not able to update.
        """

        records = self.db.get_table()
        index = -1

        for i in range(0, len(records)):
            if str(records[i]["id"]) == str(id):
                index = i

        if index == -1:
            return False

        records[index]["status"] = status
        self.db.update_cell(index, 'status', status)

        return records[index]

    def successful(self, id):
        """
        Mark a parameter set as successfully completed.

        Args:
            id (str): the id of the parameter set to use
        
        Returns:
            The new parameter set that has been updated or False if not able to update.
        """

        records = self.db.get_table()
        index = -1

        # Remove id from local cache
        if self.config:
            self.config.update(key='last-test', value=None)

        for i in range(0, len(records)):
            if str(records[i]["id"]) == str(id):
                index = i

        if index == -1:
            return False

        records[index]["status"] = "successful"
        if 'end-time' in records[index]:
            records[index]["end-time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.db.update_row(index, records[index])

        _log.info('Test %s marked as successful' % str(id))
        
        return records[index]

    def failed(self, id, err=''):
        """
        Mark a parameter set as failed to completed.
        
        Args:
            id (str): the id of the parameter set to use
            err (str): the error message.  Empty by default.
        
        Returns:
            The new parameter set that has been updated or False if not able to update.
        """

        records = self.db.get_table()
        index = -1

        for i in range(0, len(records)):
            if str(records[i]["id"]) == str(id):
                index = i
                
        if index == -1:
            return None

        records[index]["status"] = "failed"
        if 'end-time' in records[index]:
            records[index]["end-time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 'comments' in records[index]:
            records[index]["comments"] += " failed{ " + err + " };"

        self.db.update_row(index, records[index])

        _log.info('Test %s marked as failed with message %s.' % (str(id), str(err)))
        
        return records[index]
