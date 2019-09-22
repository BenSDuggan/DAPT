"""
Config
====== 

Class that allows for reading and modification of a config file.
"""

class Config:
    """
        Class which loads and allows for editing of a config file

        Args:
            path (string): path to config file
    """
    def __init__(self, path):
        self.path = path
        self.config = self.readConfig(self.path)
    
    def read_config(self):
        """
            Reads the file with path set to self.path

            Returns:
                Dictionary of config file
        """

        self.config = Config.readConfig(self.path)
        return self.config

    def change_config(self, key, value):
        """
            Change value for a given key in the config file

            Args:
                key (string): key to be changed
                value (string): value to inserted at key

            Returns:
                Dictionary of config file
        """

        self.config[key] = value

        try:
            Config.changeConfig(self.path, key, value)
        except ValueError:
            print("Can not update file.")

        return self.config

    @staticmethod
    def readConfig(path):
        """
            Reads in the config file and interprets it as a dictionary

            Args:
                path (string): path to config file

            Returns:
                Dictionary of config file
        """

        f = open(path, 'r').readlines()
        types = [int, float, str]
        config = {}
        for i in range(0, len(f)):
            f[i] = f[i].replace("\n", "")

            if f[i].split(":")[1] == 'None':
                config[f[i].split(":")[0]] = None
                continue
            elif f[i].split(":")[1] == 'True':
                config[f[i].split(":")[0]] = True
                continue
            elif f[i].split(":")[1] == 'False':
                config[f[i].split(":")[0]] = False
                continue

            for j in range(len(types)):
                try:
                    config[f[i].split(":")[0]] = types[j](f[i].split(":")[1])
                    break
                except:
                    pass

        return config


    @staticmethod
    def changeConfig(path, key, value):
        """ 
            Change value for a given key in the given file path

            Args:
                path (string): the path to the config file
                key (string): key to be changed
                value (string): value to inserted at key

            Returns:
                Dictionary of config file
        """

        f = open(path, 'r').readlines()
        data = ""
        found = False
        for i in range(0, len(f)):
            if f[i].split(':')[0] == str(key):
                f[i] = f[i].split(':')[0] + ':' + str(value) + '\n'
                found = True
            data += f[i]

        if not found:
            data += key + ':' + value

        with open(path, 'w') as file:
            file.writelines(data)

    @staticmethod
    def create(path='config.txt'):
        """
            Creates a config file with the reserved keys inserted.

            Args:
                path (string): path where config file will be writen
        """
        default = "lastTest:None\nuserName:None\nspreedsheetID:None\nclient_id:None\nclient_secret:None\nboxFolderID:None\nresetTime:None\nnumOfRuns:None\ncomputerStrength:None\naccessToken:None\nrefressToken:None"
        with open(path, 'w') as file:
            file.writelines(default)

    @staticmethod
    def safe(path="config.txt"):
        """
            Safe config file by removing accessToken and refressToken.

            Args:
                path (string): path where config file will be writen
        """
        data = Config.readConfig(path)
        if data["accessToken"]:
            data["accessToken"] = ""
            Config.changeConfig(path, "accessToken", "")
        if data["refressToken"]:
            data["refressToken"] = ""
            Config.changeConfig(path, "refressToken", "")

if __name__ == '__main__':
    print(Config.readConfig('config.txt'))
    config = Config('config.txt')
    config.change_config('lastTest', 'k')
    print(config.config) 