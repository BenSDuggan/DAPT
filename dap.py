'''
    Ben Duggan
    1/18/19
    Main script to run distributed parameter testing
'''

import datetime
class Param:
    def __init__(self, config_path, sheet):
        self.path = "DistributedAutomaticParameterTesting/"

        self.sheet = sheet

        self.config_path=config_path
        self.config = self.read_config(config_path) 

        if self.config['numOfRuns']:
            self.count = 0

    def requestParameters(self):
        if self.config['numOfRuns']:
            if int(self.config['numOfRuns']) == -1 or self.count < int(self.config['numOfRuns']):
                    self.count += 1
            else:
                return None

        records = self.sheet.getRecords()

        if "lastTest" in self.config and self.config["lastTest"] != "None":
            print("Using lastTest from config.txt")
            for i in range(0, len(records)):
                if str(self.config["lastTest"]) == str(records[i]["id"]):
                    if "startTime" in records[i]:
                        records[i]["startTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        self.sheet.update_cell(i, 'startTime', records[i]["startTime"])
                    if "performedBy" in records[i]:
                        records[i]["performedBy"] = self.config["userName"]
                        self.sheet.update_cell(i, 'performedBy', self.config["userName"])

                    return records[i]

        for i in range(0, len(records)):
            if len(records[i]["status"]) == 0:
                try:
                    if int(self.config['computerStrength']) < int(records[i]["computerStrength"]):
                        continue
                except:
                    pass

                if "status" in records[i]:
                    records[i]["status"] = "in progress"
                    self.sheet.update_cell(i, 'status', "in pogress")
                if "startTime" in records[i]:
                    records[i]["startTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.sheet.update_cell(i, 'startTime', records[i]["startTime"])
                if "performedBy" in records[i]:
                    records[i]["performedBy"] = self.config["userName"]
                    self.sheet.update_cell(i, 'performedBy', self.config["userName"])

                # Save id to local cache
                self.change_config("lastTest", str(records[i]["id"]))

                return records[i]

        return None

    def updateStatus(self, id, status):
        records = self.sheet.getRecords()
        index = -1

        # Remove id from local cache

        for i in range(0, len(records)):
            if str(records[i]["id"]) == str(id):
                index = i

        if index == -1:
            return None

        records[index]["status"] = status
        self.sheet.update_cell(index, 'status', status)

        return records[index]

    def parameterSuccessful(self, id):
        records = self.sheet.getRecords()
        index = -1

        # Remove id from local cache
        self.change_config("lastTest", "None")

        for i in range(0, len(records)):
            if str(records[i]["id"]) == str(id):
                index = i

        if index == -1:
            return None

        if 'status' in records[index]:
            records[index]["status"] = "finished"
            self.sheet.update_cell(index, 'status', "finished")
        if 'endTime' in records[index]:
            records[index]["endTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.sheet.update_cell(index, 'endTime', records[index]["endTime"])

        return records[index]

    def parameterFailed(self, id):
        records = self.sheet.getRecords()
        index = -1

        for i in range(0, len(records)):
            if str(records[i]["id"]) == str(id):
                index = i

        if index == -1:
            return None

        if 'status' in records[index]:
            records[index]["status"] = ""
            self.sheet.update_cell(index, 'status', '')
        if 'endTime' in records[index]:
            records[index]["endTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.sheet.update_cell(index, 'endTime', records[index]['endTime'])
        if 'comments' in records[index]:
            records[index]["comments"] += " failed;"
            self.sheet.update_cell(index, 'comments', records[index]["comments"])

        return records[index]

    def checkForDBErrors(self):
        records = self.sheet.getRecords()

        if len(records) > 0:
            if 'startTime' not in records[1] or 'resetTime' not in self.config:
                return None

        for i in range(0, len(records)):
            if len(records[i]["startTime"]) > 0 and ((datetime.datetime.now()-datetime.datetime.strptime(records[i]["startTime"], '%Y-%m-%d %H:%M:%S')).total_seconds() > int(self.config["resetTime"])):
                print("\"", records[i], "\" hasn't been marked as complete after running for: ", int((datetime.datetime.now()-datetime.datetime.strptime(records[i]["startTime"], '%Y-%m-%d %H:%M:%S')).total_seconds()), " seconds. It has been marked as still needing to be ran.")

                if 'comments' in records[i]:
                    records[i]["comments"] += "test possibly crashed"
                    self.sheet.update_cell(i, 'comments', records[i]["comments"])
                if 'status' in records[i]:
                    self.sheet.update_cell(i, 'status', '')
                if 'startTime' in records[i]:
                    self.sheet.update_cell(i, 'startTime', '')
                return records
        return None    


