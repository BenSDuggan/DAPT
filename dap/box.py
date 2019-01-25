'''
    Ben Duggan
    10/30/18
    Script for getting box access token and uploading files
'''

import os, time
from boxsdk import *
from flask import *

class Box:
    def __init__(self, config):
        self.config = config
        self.conf = config.config

        self.access_token = None
        self.refresh_token = None
        self.client = None
        self.refreshTime = None

        ''' START - Flask web server used for auth'''
        self.app = Flask(__name__)

    # The method called to start the server
    def startServer(self):
        print("Starting server.  Go to 127.0.0.1:5000 to authenticate box.  It can only be ended by completing authentification or going to 127.0.0.1:5000/end")
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/return', 'return', self.capture)
        self.app.add_url_rule('/end', 'end', self.end)
        self.app.run()
        print("Server stoped")
        return self.client.user(user_id='me').get()['login']

    # This is the index of the web server and serves as the start point for authentication
    def index(self):
        self.oauth = OAuth2(
            client_id=self.conf['client_id'],
            client_secret=self.conf['client_secret']
        )

        self.auth_url, self.csrf_token = self.oauth.get_authorization_url("http://127.0.0.1:5000/return")

        return '<h1>Welcome to box auth</h1> This web server is used to interface with the box API.  Click the link below to securely login on box.' + '<a href="'+self.auth_url+'">Click here to authenticate your box account </a>'
    
    # This page is called using a GET request by the Box API and gives the access token and refresh token needed to upload files to box
    def capture(self):
        # Capture auth code and csrf token via state
        code = request.args.get('code')
        state = request.args.get('state')

        # If csrf token matches, fetch tokens
        assert state == self.csrf_token
        self.access_token, self.refresh_token = self.oauth.authenticate(code)

        self.client = Client(self.oauth)

        self.refreshTime = time.time() + 60*60

        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

        if self.config:
            self.config.change_config('userName',self.client.user(user_id='me').get()['login'])

        return 'You are now logged in as: ' + self.client.user(user_id='me').get()['login'] + '<br><strong>The server has been shutdown and the normal script is resuming.</strong><a href="http://127.0.0.1:5000">Click to go to index (assuming server restarted)</a>'

    # When the user goes to /end the server shuts down
    def end(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 'Server shutting down...<br> Getting back to the main python script.'

    ''' END - Flask web server used for auth'''

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