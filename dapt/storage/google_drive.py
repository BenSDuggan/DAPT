"""
.. _google_drive:

Google Drive
============



"""

import logging, json, io, os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaIoBaseDownload

from . import base

_log = logging.getLogger(__name__)

class Google_Drive(base.Storage):
    """
    Download, upload, move, and delete files or folders from Google Drive.

    Args:
        creds_path (str): the path to the file containing the Google API credentials.  Default is ``credentials.json``.
        config (Config): a Config object with the associated config file to be used
    """

    def __init__(self, **kwargs):
        #self.SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self._creds = None
        self.creds_path = None
        self.config = None
        self.service = None

        if 'config' in kwargs:
            self.config = kwargs['config']
            if self.config.has_value('google-drive'):
                if self.config.has_value(['google-drive', 'creds-path']):
                    self.creds_path = self.config['google-drive']['creds-path']
                if self.config.has_value(['google-drive', 'creds']):
                    creds = json.loads(self.config['google-drive']['creds'])
                    if type(creds) is dict and "refresh_token" in creds and "client_id" in creds and  "client_secret" in creds:
                        self._creds = Credentials.from_authorized_user_info(creds, self.SCOPES)
                        _log.info('Loaded credentials from Config.')
        if 'creds_path' in kwargs:
            self.creds_path = kwargs['creds_path']

    def connect(self):
        """
        Allows you to sign into your Google account through the internet browser.  This should automatically open the browser up.

        Returns:
            True if the connection was successful and False otherwise.
        """

        # Check the current creds and try to update them
        if self._creds and not self._creds.valid and self._creds.refresh_token:
            _log.debug('Attempting to update the internal creds')
            self._creds.refresh(Request())
            self.service = build('drive', 'v3', credentials=self._creds)
            
            self._update_config()
            return self._valid_creds()

        # Ask the user to log in
        _log.debug('Asking the user to sign in and get new creds')
        flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, self.SCOPES)
        self._creds = flow.run_local_server(port=0)
        self.service = build('drive', 'v3', credentials=self._creds)

        self._update_config()
        return self._valid_creds()

    def _update_config(self):
        """
        Update the Config object to reflect the current state of the code.  If there is no config object, do nothing.
        """

        if self.config:
            if self.config.has_value(['google-drive', 'creds']):
                self.config['google-drive']['creds'] = self._creds.to_json()
            
            self.config.update()


    def _valid_creds(self):
        """
        Check to see if the credentials are valid.

        Returns:
            True if the credentials are valid and False otherwise.
        """

        if self._creds:
            return self._creds.valid
        return False

    def _get_metadata(self, file_id):
        """
        Get the Google Drive metadata for the given file ID.

        Args:
            file_id (str): The file ID of the metadata to get

        Returns:
            The metadata as a ``dict``.
        """

        return self.service.files().get(fileId=file_id).execute()

    def download_file(self, file_id, filename=None):
        """
        Download the file at the given file_id to the given path.  This will only download binary files such as Microsoft Docs, PDFs, PNGs, MP4, etc.  This method is not capable of downloading Google products such as Google Docs and Google Sheets.

        Args:
            file_id (str): The file identification to be downloaded
            path (str): The path where the folder should be saved
            filename (str): The name of the file that should be saved.  If None then it will be the name of the file on Drive

        Returns:
            True if successful and False otherwise
        """
        
        request = self.service.files().get_media(fileId=file_id)
        metadata = self._get_metadata(file_id)

        if filename is None:
            metadata = self.service.files().get(fileId=file_id).execute()
            filename = metadata["name"]

        if "application/vnd.google-apps" in metadata["mimeType"]:
            _log.warn('Only binary files can be downloaded from Google Drive.  Files such as Google Docs cannot.')
            return False

        fh = io.FileIO(filename, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            _log.info("Downloading \"%s\": %d%%." % (metadata["name"], int(status.progress() * 100)))

        return done

    def download_folder(self, file_id, path='.', foldername=None):
        """
        Download the folder at the given file_id to the given path.

        Args:
            file_id (str): The folder identification to be downloaded
            path (str): The path where the folder should be saved
            foldername (str): The name of the destination folder

        Returns:
            True if successful and False otherwise
        """

        files = []
        
        metadata = self._get_metadata(file_id)

        if foldername is None:
            foldername = metadata["name"]

        page_token = None
        while True:
            response = self.service.files().list(q="'%s' in parents" % file_id, pageSize=1, fields='nextPageToken, files(id, name, mimeType)', pageToken=page_token).execute()

            files += response.get('files', [])

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        print(files)

        #print(self._get_metadata(file_id))

        return True

        os.mkdir(foldername)

        files = []

        page_token = None
        while True:
            if page_token:
                param['pageToken'] = page_token
            
            children = self.service.children().list(folderId=file_id, maxResults=1).execute()
            files.append(children.get('items', []))
            
            page_token = children.get('nextPageToken')
            if not page_token:
                break
        
        print(files)
        return False

        for file in files:
            if "application/vnd.google-apps.folder" in metadata["mimeType"]:
                return self.download_folder(file["id"], path)
            else:
                _log.warn('You did not provide the file ID of a Google Drive folder.')
                return False

    def delete_file(self, file_id):
        """
        Delete the the given file.

        Args:
            file_id (str): The file identification to be downloaded

        Returns:
            True if successful and False otherwise
        """
        pass

    def delete_folder(self, folder_id):
        """
        Delete the given folder.

        Args:
            folder_id (str): The folder identification to be downloaded

        Returns:
            True if successful and False otherwise
        """
        pass

    def rename_file(self, file_id, name):
        """
        Rename the given file.

        Args:
            file_id (str): The file identification to be downloaded
            name (str): The new name of the file or folder

        Returns:
            True if the file or folder was renamed, False otherwise.
        """
        pass

    def rename_folder(self, folder_id, name):
        """
        Rename the given folder.

        Args:
            folder_id (str): The folder identification to be downloaded
            name (str): The new name of the file or folder

        Returns:
            True if the file or folder was renamed, False otherwise.
        """
        pass

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
        pass

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
        pass