"""
Box
=== 

Class that allows for access to the box API and methods to directly upload files
"""

import os, time
from boxsdk import *
from flask import *

class Box:
    """
        Class which allows for connection to box API

        Args:
            config (Config): Config object with config file
    """
    def __init__(self, config=None):
        self.config = config
        self.conf = config.config
        
        self.access_token = None
        self.refresh_token = None
        self.client = None
        self.refreshTime = None
        self.oauth = OAuth2(
            client_id=self.conf['client_id'],
            client_secret=self.conf['client_secret']
        )
        
        self.app = Flask(__name__)


    def connect(self):
        """
            Tries to connect to box using arguments provided in Config and starts server for authorization if not.
            
            Returns:
                Box client if successful
        """

        if self.config and len(self.conf['accessToken']) > 0 and len(self.conf['refressToken']) > 0: 
            try:
                print('Trying to get new access and refresh token from ' + self.config.path)
                self.oauth._refresh_token = self.conf['refressToken']
                self.access_token, self.refresh_token = self.oauth._refresh(self.conf['accessToken'])
                self.client = Client(self.oauth)
                self.refreshTime = time.time() + 60*60

                if self.config:
                    self.config.change_config('userName',self.client.user(user_id='me').get()['login']) #Save username to config
                    self.config.change_config('accessToken',self.access_token) #Save access token to config
                    self.config.change_config('refressToken',self.refresh_token) #Save refresn token to config

                print('Got new access and refresh token from existing')
                return

            except Exception as e:
                print(e)

        print('Starting server.  Go to the URL below to activate box functionality.  If you are on a server you will need to run this code on your computer, get the access and refresh token and then add them to the config file.')
        return self.startServer()

    def startServer(self):
        """
            Method that starts flask to start authorization process

            Returns:
                Box client which can be used to access authorized user data
        """

        print("Starting server.  Go to 127.0.0.1:5000 to authenticate box.  It can only be ended by completing authentification or going to 127.0.0.1:5000/end")
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/return', 'return', self.capture)
        self.app.add_url_rule('/end', 'end', self.end)
        self.app.run()
        print("Server stoped")
        return self.client

    def index(self):
        """
            Flask page: index of the web server and serves as the start point for authentication

            Returns:
                String containing HTML to be displayed
        """
        self.auth_url, self.csrf_token = self.oauth.get_authorization_url("http://127.0.0.1:5000/return")

        return '<h1>Welcome to box auth</h1> This web server is used to interface with the box API.  Click the link below to securely login on box.' + '<a href="'+self.auth_url+'">Click here to authenticate your box account </a>'
    
    def capture(self):
        """
            Flask page: box redirect url which contains the code and state used to get access and refress token

            Returns:
                String containing HTML to be displayed with box login credentials
        """

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
            self.config.change_config('userName',self.client.user(user_id='me').get()['login']) #Save username to config
            self.config.change_config('accessToken',self.access_token) #Save access token to config
            self.config.change_config('refressToken',self.refresh_token) #Save refresn token to config


        return 'You are now logged in as: ' + self.client.user(user_id='me').get()['login'] + '<br><strong>The server has been shutdown and the normal script is resuming.</strong><br>access token: '+self.access_token+'<br>refresh token: '+self.refresh_token+'<br><a href="http://127.0.0.1:5000">Click to go to index (assuming server restarted)</a>'

    def end(self):
        """
            Flask page: shuts down flask server

            Returns:
                String containing HTML to be displayed
        """

        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 'Server shutting down...<br> Getting back to the main python script.'

    def updateTokens(self, access_token):
        """
            Refresh the access and refresh token given a valid access token

            Args:
                access_token (string): box access token to be refreshed

            Returns:
                Box client
        """

        self.access_token, self.refresh_token = self.oauth.refresh(access_token)
        self.client = Client(self.oauth)
        self.refreshTime = time.time() + 60*60

        if self.config:
            self.config.change_config('userName',self.client.user(user_id='me').get()['login']) #Save username to config
            self.config.change_config('accessToken',self.access_token) #Save access token to config
            self.config.change_config('refressToken',self.refresh_token) #Save refresn token to config

        return self.client

    def uploadFile(self, folderID, path, name):
        """
            Upload a file to box using the current client

            Args:
                folderID (string): the box folder ID that the file should be added to (found in URL)
                path (string): the path to the file on your local machine
                file (string): the name of the file you wish to upload
        """

        # If the access token is expired (or about to be), then update it
        if self.refreshTime < time.time() + 5:
            self.updateTokens(self.access_token)
        print(self.client.folder(folderID).upload(os.getcwd()+path, name))

    
    

if __name__ == '__main__':
    os.chdir("../")
    app.run()

    items = client.folder(folder_id='0').get_items(limit=100, offset=0)

    for i in items:
        print(i)

    #uploadFile('\\DistributedAutomaticParameterTesting\\', "testPayload.zip")