"""
    Param
    =====

    Interact with the database to get and manage paramater sets.
"""

import datetime
#import config

class Param:
    def __init__(self, database, config=None):
        """
            Create a Param instance with a database and optional config file.

            Args:
                database (Database): a Database instance (such as Sheets or Delimited_file)
                config (Config): a config object which allows for more features.  This is optional.
        """

        self.db = database

        if self.config == None:
            pass
        else:
            self.config = config
            self.conf = config.config

            if self.conf['numOfRuns']:
                self.count = 0

    def next_parameters(self):
        """
            Get the next paramater set if one exists
            
            Returns:
                An OrderedDict containing the key-value pairs from that paramater set or None if there are no more to sets.
        """

        # Do we have a config file
        if self.config not None:
            if self.config not None and self.conf['numOfRuns']:
                if int(self.conf['numOfRuns']) == -1 or self.count < int(self.conf['numOfRuns']):
                        self.count += 1
                else:
                    return None

            records = self.db.get_table()

            if "lastTest" in self.conf and self.conf["lastTest"] != "None":
                print("Using lastTest from config.txt")
                for i in range(0, len(records)):
                    if str(self.conf["lastTest"]) == str(records[i]["id"]):
                        if "startTime" in records[i]:
                            records[i]["startTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            self.db.update_cell(i, 'startTime', records[i]["startTime"])
                        if "performedBy" in records[i]:
                            records[i]["performedBy"] = self.conf["userName"]
                            self.db.update_cell(i, 'performedBy', self.conf["userName"])

                        return records[i]

        records = self.db.get_table()

        for i in range(0, len(records)):
            if len(records[i]["status"]) == 0:
                try:
                    if int(self.conf['computerStrength']) < int(records[i]["computerStrength"]):
                        continue
                except:
                    pass

                if "status" in records[i]:
                    records[i]["status"] = "in progress"
                    self.db.update_cell(i, 'status', "in pogress")
                if "startTime" in records[i]:
                    records[i]["startTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.db.update_cell(i, 'startTime', records[i]["startTime"])
                if "performedBy" in records[i]:
                    records[i]["performedBy"] = self.conf["userName"]
                    self.db.update_cell(i, 'performedBy', self.conf["userName"])

                # Save id to local cache
                self.config.change_config("lastTest", str(records[i]["id"]))

                return records[i]

        return None

    def update_status(self, id, status):
        """
            Update the status of the selected paramater.  If status is not included in the paramater set keys then nothing will be updated.

            Args:
                id (str): the id of the paramater set to use
            
            Returns:
                The new paramater set that has been updated or False if not able to update.
        """

        records = self.db.get_table()
        index = -1

        # Remove id from local cache

        for i in range(0, len(records)):
            if str(records[i]["id"]) == str(id):
                index = i

        if index == -1:
            return False

        if 'status' in records[index]:
            records[index]["status"] = status
            self.db.update_cell(index, 'status', status)

            return records[index]
        else:
            return False

    def successful(self, id):
        """
            Mark a paramater set as successfully completed.

            Args:
                id (str): the id of the paramater set to use
            
            Returns:
                The new paramater set that has been updated or False if not able to update.
        """

        records = self.db.get_table()
        index = -1

        # Remove id from local cache
        if self.config not None:
            self.config.change_config("lastTest", "None")

        for i in range(0, len(records)):
            if str(records[i]["id"]) == str(id):
                index = i

        if index == -1:
            return False

        if 'status' in records[index]:
            records[index]["status"] = "finished"
            self.db.update_cell(index, 'status', 'finished')
        if 'endTime' in records[index]:
            records[index]["endTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.db.update_cell(index, 'endTime', records[index]["endTime"])
        
        return records[index]

    def failed(self, id, err=''):
        """
            Mark a paramater set as failed to completed.
            
            Args:
                id (str): the id of the paramater set to use
                err (str): the error message.  Empty by default.
            
            Returns:
                The new paramater set that has been updated or False if not able to update.
        """

        records = self.db.get_table()
        index = -1

        for i in range(0, len(records)):
            if str(records[i]["id"]) == str(id):
                index = i
                
        if index == -1:
            return None

        if 'status' in records[index]:
            records[index]["status"] = ""
            self.db.update_cell(index, 'status', '')
        if 'endTime' in records[index]:
            records[index]["endTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.db.update_cell(index, 'endTime', records[index]['endTime'])
        if 'comments' in records[index]:
            records[index]["comments"] += " failed\{" + err + "\};"
            self.db.update_cell(index, 'comments', records[index]["comments"])

        return records[index]
