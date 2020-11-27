"""
.. _box:

Box
=== 

Class that allows for access to the box API and methods to directly upload files.  If you wish to use the Box API you should view the `install </install/box-install.html>`_.

Authentication
--------------

In order for the Box API to work, it needs to get a user specific access and refresh token.  Box provides access tokens to users which are a session key.  They remain active for one hour at which time they must be refreshed using the refresh token.  Once a new access and refresh token has been given, the old one will no longer work.

The tokens can be provided in three  ways.  First, you can run ``Box(...).connect()`` which will start a flask webserver.  You can then proceed to `<127.0.0.1:5000>`_ and log in with your Box username and password.  This is done securely through Box and you username and password cannot be extracted.  Second, you can insert the access and refresh token in the config file.  Then the Box class will use these tokens.  The final way to provide the tokens is by directly passign them to ``Box(...).connect(access_token=<your access token>, refresh_token=<your refresh token>)``.

On a server, where you have no access to a web browser, you will need to get the tokens using a computer which has a web browser.  You can then place those tokens in the config file or directly pass them to the ``connect()`` method.

.. _box-config:

Config
------

The best way to use Box is with a configuration file.  Box attributes can be added to the config file as a JSON object which is the value for the key ``box``.  An sample config file for box is shown bellow.

.. code-block:: json
    
    {
        "box" : {
            "client_id" : "xxx",
            "client_secret" : "xxx",
            "access_token" : "xxx",
            "refresh_token" : "xxx",
            "refresh_time" : "xxx"
        }
    }

"""

import os, time, shutil
import logging as lg
from pathlib import Path

from boxsdk import *
from flask import *

from . import base

_log = lg.getLogger(__name__)

class Box(base.Storage):
    """
    Class which allows for connection to box API.  You must either provide a Config object or client_id and client_secret.

    Keyword Args:
        config (Config): A Config object which contains the client_id and client_secret. 
        client_id (str): The Box client ID.
        client_secret (str): The Box client secret.
    """

    def __init__(self, *args, **kwargs):
        self.config = None
        self.client_id = None
        self.client_secret = None
        self._access_token = None
        self._refresh_token = None
        self._csrf_token = None
        self.refresh_time = None
        self.client = None
        self.app = None

        if 'config' in kwargs:
            self.config = kwargs['config']
            if self.config.has_value('box'):
                box_conf = self.config.config['box']
                if 'client-id' in box_conf:
                    self.client_id = box_conf['client-id']
                if 'client-secret' in box_conf:
                    self.client_secret = box_conf['client-secret']
        if 'client-id' in kwargs:
            self.client_id = kwargs['client-id']
        if 'client-secrent' in kwargs:
            self.client_secret = kwargs['client-secret']
        
        if self.client_id is None or self.client_secret is None:
            raise AttributeError('The client-id and client-secret must be provided.  They can be provided directly or using a Config.')

        self.oauth = OAuth2(client_id=self.client_id, client_secret=self.client_secret)

    def connect(self, access_token = None, refresh_token = None):
        """
        Tries to connect to box using arguments provided in Config and starts server for authorization if not.

        Args:
            access_token (str): Optional argument that allows DAPT to connect to box without going through web authentication (assuming refresh_token is given and not expired).
            refresh_token (str): Optional argument that allows DAPT to connect to box without going through web authentication (assuming access_token is given and not expired).
        
        Returns:
            Box client if successful
        """

        # Check to see if the user gave us the access and refresh token
        if access_token and refresh_token:
            self.oauth._refresh_token = refresh_token
            self._access_token, self._refresh_token = self.oauth._refresh(access_token)
            self.client = Client(self.oauth)
            self.refresh_time = time.time() + 60*60

            self._update_config()

            return

        # If not, then we check to see if the access and refresh token are in the config file.
        if self.config and self.config.has_value(['box','access-token']) and self.config.has_value(['box','refresh-token']):
            try:
                print('Trying to get new access and refresh token from ' + self.config.path)
                self.oauth._refresh_token = self.config.config['refresh-token']
                self._access_token, self._refresh_token = self.oauth._refresh(self.config['box']['access-token'])
                self.client = Client(self.oauth)
                self.refresh_time = time.time() + 60*60

                print('Got new access and refresh token from existing')
                return

            except Exception as e:
                print(e)

        self.app = Flask(__name__)
        print('Starting server.  Go to the URL below to activate box functionality.  If you are on a server you will need to run this code on your computer, get the access and refresh token and then add them to the config file.')
        return self._start_server()

    def _start_server(self):
        """
        Method that starts flask to start authorization process

        Returns:
            Box client which can be used to access authorized user data
        """

        print("Starting server.  Go to 127.0.0.1:5000 to authenticate box.  It can only be ended by completing authentication or going to 127.0.0.1:5000/end")
        self.app.add_url_rule('/', 'index', self._index)
        self.app.add_url_rule('/return', 'return', self._capture)
        self.app.add_url_rule('/end', 'end', self._end)
        self.app.run()
        print("Server stoped")
        return self.client

    def _index(self):
        """
        Flask page: index of the web server and serves as the start point for authentication

        Returns:
            String containing HTML to be displayed
        """
        self.auth_url, self._csrf_token = self.oauth.get_authorization_url("http://127.0.0.1:5000/return")

        return '<h1>Welcome to box auth</h1> This web server is used to interface with the box API.  Click the link below to securely login on box.' + '<a href="'+self.auth_url+'">Click here to authenticate your box account </a>'
    
    def _capture(self):
        """
        Flask page: box redirect url which contains the code and state used to get access and refresh token

        Returns:
            String containing HTML to be displayed with box login credentials
        """

        # Capture auth code and csrf token via state
        code = request.args.get('code')
        state = request.args.get('state')

        # If csrf token matches, fetch tokens
        assert state == self._csrf_token
        self._access_token, self._refresh_token = self.oauth.authenticate(code)

        self.client = Client(self.oauth)

        self.refresh_time = time.time() + 60*60

        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

        self._update_config()
        
        return 'You are now logged in as: ' + self.client.user(user_id='me').get()['login'] + '<br><strong>The server has been shutdown and the normal script is resuming.</strong><br>access token: '+self._access_token+'<br>refresh token: '+self._refresh_token+'<br><a href="http://127.0.0.1:5000">Click to go to index (assuming server restarted)</a>'

    def _end(self):
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

    def _update_config(self):
        """
        Update the Config object to reflect the current state of the code.  If there is no config object, do nothing.
        """

        if self.config:

            if self.config.has_value('performed-by') and self.client is not None:
                self.config['performed-by'] = self.client.user(user_id='me').get()['login']
            
            if self.config.has_value('box'):
                box_conf = self.config['box']

                if 'client-id' in box_conf:
                    self.config['box']['client-id'] = self.client_id
                if 'client-secret' in box_conf:
                    self.config['box']['client-secret'] = self.client_secret
                if 'access-token' in box_conf:
                    self.config['box']['access-token'] = self._access_token
                if 'refresh-token' in box_conf:
                    self.config['box']['refresh-token'] = self._refresh_token
                if 'refresh_time' in box_conf:
                    self.config['box']['refresh_time'] = self.refresh_time
            
            self.config.update()

    def _check_tokens(self):
        """
        Check to see if the tokens need to be refreshed.

        Returns:
            True if the token was refreshed and False otherwise.
        """

        if self.refresh_time < time.time() + 5:
            self.update_tokens(self._access_token)
            self._update_config()
            return True
        return False

    def update_tokens(self, access_token):
        """
        Refresh the access and refresh token given a valid access token

        Args:
            access_token (string): box access token to be refreshed

        Returns:
            Box client
        """

        self._access_token, self._refresh_token = self.oauth.refresh(access_token)
        self.client = Client(self.oauth)
        self.refresh_time = time.time() + 60*60

        self._update_config()

        return self.client

    def download_file(self, file_id, path='.', overwrite=True):
        """
        Download the file at the given file_id to the given path.

        Args:
            file_id (str): The file identification to be downloaded
            path (str): The path where the file should be saved
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if successful and False otherwise
        """
        self._check_tokens()

        file = self.client.file(file_id)
        file_info = file.get()
        file_path = Path(path)

        # Assume that the given path should be used as the name if it has a suffix
        if len(file_path.suffix) == 0:
             file_path /= file_info.name

        # Check to see if there is already an object at the path
        if file_path.exists() and not overwrite:
            raise FileExistsError

        contents = file.content()
        with open(file_path, 'wb') as f:
            f.write(contents)
            f.close()

        return True
    
    def download_folder(self, folder_id, path='.', overwrite=True):
        """
        Download the folder at the given file_id to the given path.

        Args:
            folder_id (str): The folder identification to be downloaded
            path (str): The path where the file should be saved
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if successful and False otherwise
        """

        self._check_tokens()

        root_folder = self.client.folder(folder_id=folder_id)
        root_folder_info = root_folder.get()
        items = root_folder.get_items()
        curr_path = Path(path) / root_folder_info.name

        if curr_path.is_dir():
            if overwrite and len(os.listdir(curr_path)) > 0:
                shutil.rmtree(curr_path)
                os.mkdir(curr_path)
            else:
                raise OSError   
        else:
            os.mkdir(curr_path)

        for item in items:
            if item.type == 'folder':
                self.download_folder(item.id, curr_path)
            elif item.type == 'file':
                self.download_file(item.id, curr_path / item.name)
            else:
                raise TypeError

        return True

    def delete_file(self, file_id):
        """
        Delete the the given file.

        Args:
            file_id (str): The file identification to be downloaded

        Returns:
            True if successful and False otherwise
        """

        return self.client.file(file_id).delete()

    def delete_folder(self, folder_id):
        """
        Delete the given folder.

        Args:
            folder_id (str): The folder identification to be downloaded

        Returns:
            True if successful and False otherwise
        """

        return self.client.folder(folder_id).delete()

    def rename_file(self, file_id, name):
        """
        Rename the given file.

        Args:
            file_id (str): The file identification to be downloaded
            name (str): The new name of the file or folder

        Returns:
            True if the file or folder was renamed, False otherwise.
        """

        renamed_file = self.client.file(file_id).rename(name)

        if renamed_file.id == file_id and renamed_file.name == name:
            return True
        else:
            return False

    def rename_folder(self, folder_id, name):
        """
        Rename the given folder.

        Args:
            folder_id (str): The folder identification to be downloaded
            name (str): The new name of the file or folder

        Returns:
            True if the file or folder was renamed, False otherwise.
        """
        
        renamed_folder = self.client.folder(folder_id).rename(name)

        if renamed_folder.id == folder_id and renamed_folder.name == name:
            return True
        else:
            return False

    def upload_file(self, folder_id, path, name=None, overwrite=True):
        """
        Upload a file to the given folder.

        Args:
            folder_id (str): The folder identification to be downloaded
            path (str): The path to the file or folder to be uploaded
            name (str): The name the file or folder should be saved with.  If None then the leaf of the path is used as the name.
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if the upload was successful and False otherwise.
        """

        self._check_tokens()
        
        parent_folder = self.client.folder(folder_id)

        if name is None:
            name = Path(path).name

        # Check if the a file with `name` exists in the folder being uploaded to
        filter_function = lambda x : (x.name == name and x.type == 'file')
        exists = list(filter(filter_function, parent_folder.get_items()))

        # Remove the file, if it exists and the user has set overwrite to True
        if len(exists) == 1:
            if overwrite:
                self.delete_file(exists[0].id)
            else:
                raise FileExistsError
        elif len(exists) > 1:
            # This is just a sanity check
            raise Exception('More than one file with the upload name were found.  Not sure what to do so crashing.')

        new_file = parent_folder.upload(path, name)

        # Did the file get uploaded correctly
        if isinstance(new_file, file.File):
            return True
        else:
            return False
    
    def upload_folder(self, folder_id, path, name=None, overwrite=True):
        """
        Upload a folder to the given folder.

        Args:
            folder_id (str): The folder identification to be downloaded
            path (str): The path to the file or folder to be uploaded
            name (str): The name the file or folder should be saved with.  If None then the leaf of the path is used as the name.
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if the upload was successful and False otherwise.
        """
        
        self._check_tokens()
        
        parent_folder = self.client.folder(folder_id)

        if name is None:
            name = Path(path).name

        # Check if the a folder with `name` exists in the folder being uploaded to
        filter_function = lambda x : (x.name == name and x.type == 'folder')
        exists = list(filter(filter_function, parent_folder.get_items()))

        # Remove the folder, if it exists and the user has set overwrite to True
        if len(exists) == 1:
            if overwrite:
                self.delete_folder(exists[0].id)
            else:
                raise Exception('A folder with the upload name, %s, already exists.  Use `overwrite=True` to force an overwrite of this folder.' % str(name))
        elif len(exists) > 1:
            # This is just a sanity check
            raise Exception('More than one folder with the upload name were found.  Not sure what to do so crashing.')

        # Create the new parent folder
        parent_folder = parent_folder.create_subfolder(name)

        # Iterate over the contents of path.  Add files and recursively add folders.
        path = Path(path)
        for f in path.iterdir():
            if f.is_dir():
                self.upload_folder(parent_folder.id, f)
            elif f.is_file():
                self.upload_file(parent_folder.id, f)


