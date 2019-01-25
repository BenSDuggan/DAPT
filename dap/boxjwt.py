'''
    Ben Duggan
    10/30/18
    Script for getting box access token and uploading files
'''

import os, time
from boxsdk import *
from flask import *

class BoxJWT:
    def __init__(self, config):
        self.config = config
        self.conf = config.config

        self.access_token = None
        self.refresh_token = None
        self.client = None

    ''' START - Box upload functions '''
    def uploadFile(self, folderID, path, file):
        # If the access token is expired (or about to be), then update it
        if self.refreshTime < time.time() + 5:
            self.updateTokens(self.access_token)
        print(self.client.folder(folderID).upload(os.getcwd()+path+file, file))

    def updateTokens(self, access):
        self.access_token, self.refresh_token = self.oauth.refresh(access)
        self.client = Client(self.oauth)
        self.refreshTime = time.time() + 60*60
    ''' END - Box upload functions '''

if __name__ == '__main__':
    os.chdir("../")
    app.run()

    items = client.folder(folder_id='0').get_items(limit=100, offset=0)

    for i in items:
        print(i)

    #uploadFile('\\DistributedAutomaticParameterTesting\\', "testPayload.zip")