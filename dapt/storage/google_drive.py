"""
.. _google_drive:

Google Drive
============

Authentication
--------------

Config
------

Usage
-----

"""

import io
import json
import logging
import os
from pathlib import Path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaIoBaseDownload, MediaFileUpload

from . import base

_log = logging.getLogger(__name__)

class Google_Drive(base.Storage):
    """
    Download, upload, move, and delete files or folders from Google Drive.

    Args:
        creds_path (str): the path to the file containing the Google API credentials. 
        Default is ``credentials.json``.
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
        Allows you to sign into your Google account through the internet browser.  This should
        automatically open the browser up.

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
        Update the Config object to reflect the current state of the code.  If there is no config
        object, do nothing.
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

    def download_file(self, file_id, folder='.', name=None, overwrite=True):
        """
        Download the file at the given file_id to the given path.  This will only download binary
        files such as Microsoft Docs, PDFs, PNGs, MP4, etc.  This method is not capable of
        downloading Google products such as Google Docs and Google Sheets.

        Args:
            ile_id (str): The file identification to be downloaded
            folder (str): The directory where the file should be saved
            name (str): The name that the file should be saved as.  If None is given (default),
            then the name of the file on the resource will be used.
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if successful and False otherwise
        """
        
        request = self.service.files().get_media(fileId=file_id)
        metadata = self._get_metadata(file_id)

        if name is None:
            name = metadata["name"]

        path = Path(folder) / name

        if not base.check_overwrite_file(folder, name, overwrite, True):
            _log.warn('Could not download the file %s(%s) because a file with that name exists. Mark "overwrite" as true to overwrite the existing file.' % (file_id, name))
            return False

        if "application/vnd.google-apps" in metadata["mimeType"]:
            _log.warn('Error downloading %s(%s): Only binary files can be downloaded from Google Drive.  Files such as Google Docs cannot.' % (name, file_id))
            return False

        fh = io.FileIO(path, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            _log.info("Downloading \"%s\": %d%%." % (metadata["name"], int(status.progress() * 100)))

        return done

    def download_folder(self, file_id, folder='.', name=None, overwrite=True):
        """
        Download the folder at the given file_id to the given path.

        Args:
            ile_id (str): The file identification to be downloaded
            folder (str): The directory where the file should be saved
            name (str): The name that the file should be saved as.  If None is given (default),
            then the name of the file on the resource will be used.
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if successful and False otherwise
        """
        
        metadata = self._get_metadata(file_id)

        if name is None:
            name = metadata["name"]

        path = Path(folder) / name

        if not base.check_overwrite_folder(folder, name, overwrite, True):
            _log.warn('Could not download the folder %s(%s) because a file with that name exists.  Mark "overwrite" as true to overwrite the existing file.' % (name, file_id))
            return False
        
        files = []
        page_token = None
        while True:
            response = self.service.files().list(q="'%s' in parents" % file_id, pageSize=100, fields='nextPageToken, files(id, name, mimeType)', pageToken=page_token).execute()

            files += response.get('files', [])

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        _log.debug('Starting download of %d items in folder "%s" (%s)' % (len(files), name, file_id))

        for f in files:
            if f["mimeType"] == 'application/vnd.google-apps.folder':
                self.download_folder(f["id"], path, )
            else:
                self.download_file(f["id"], path, )

        _log.info('Finished downloading folder "%s" (%s)' % (name, file_id))

        return True

    def delete_file(self, file_id):
        """
        Delete the the given file.

        Args:
            file_id (str): The file identification to be downloaded

        Returns:
            True if successful and False otherwise
        """

        metadata = self._get_metadata(file_id)
        
        self.service.files().delete(fileId=file_id).execute()
        _log.info('Deleted file "%s"(%s).' % (metadata["name"], file_id))

    def delete_folder(self, file_id):
        """
        Delete the given folder.

        Args:
            file_id (str): The folder identification to be downloaded

        Returns:
            True if successful and False otherwise
        """
        
        metadata = self._get_metadata(file_id)
        
        self.service.files().delete(fileId=file_id).execute()
        _log.info('Deleted folder "%s"(%s).' % (metadata["name"], file_id))

    def rename_file(self, file_id, name):
        """
        Rename the given file.

        Args:
            file_id (str): The file identification to be downloaded
            name (str): The new name of the file or folder

        Returns:
            True if the file or folder was renamed, False otherwise.
        """

        metadata = self._get_metadata(file_id)

        new_name = {'name': name}
        updated_file = self.service.files().update(fileId=file_id, body=new_name, fields='name').execute()

        _log.info('Renamed file "%s"(%s) to "%s"' % (metadata["name"], file_id, name)) 

        return True

    def rename_folder(self, file_id, name):
        """
        Rename the given folder.

        Args:
            file_id (str): The folder identification to be downloaded
            name (str): The new name of the file or folder

        Returns:
            True if the file or folder was renamed, False otherwise.
        """
        
        metadata = self._get_metadata(file_id)

        new_name = {'name': name}
        updated_file = self.service.files().update(fileId=file_id, body=new_name, fields='name').execute()

        _log.info('Renamed folder "%s"(%s) to "%s"' % (metadata["name"], file_id, name)) 

        return True

    def upload_file(self, file_id, name, folder='.', overwrite=True):
        """
        Upload a file to the given folder.

        Args:
            file_id (str): The folder where the file should be saved.
            name (str): The name that the file should be uploaded.
            folder (str): The directory where the file is stored.
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if the upload was successful and False otherwise.
        """

        file_metadata = {'name':name, 'parents':[file_id]}
        path = Path(folder) / name
        mimetype = base.get_mime_type(name)

        media = MediaFileUpload(path, mimetype=mimetype, resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return True

    def upload_folder(self, file_id, name, folder='.', overwrite=True):
        """
        Upload a folder to the given folder.

        Args:
            file_id (str): The folder where the folder should be saved.
            name (str): The name that the file should be uploaded.
            folder (str): The directory where the folder is stored.
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if the upload was successful and False otherwise.
        """

        parent_folder = self.create_folder(file_id, name)
        
        path = Path(folder) / name
        for f in path.iterdir():
            if f.is_dir():
                self.upload_folder(parent_folder.get('id'), f.name, str(path))
            elif f.is_file():
                self.upload_file(parent_folder.get('id'), f.name, str(path))

        return True

    def create_folder(self, file_id, name):
        """
        Create a folder named `name` in the folder with the `file_id` given.

        Args:
            file_id (str): The file id of the parent folder to create the new folder in
            name (str): What the name of the new folder should be

        Returns:
            The file metedata if successful and None otherwise.
        """

        file_metadata = {'name':name, 'parents':[file_id], 'mimeType':'application/vnd.google-apps.folder'}

        file = self.service.files().create(body=file_metadata, fields='id').execute()

        return file