"""
.. _base-storage:

Storage base
============

This module contans classes and functions that assist with the storage APIs.  It includes the
``Storage`` class and methods to deal with overwriting files/folders.

Because the APIs of services are all different, DAPT calls the resource identification a
``file_id``.  Even if the resource is not a file, it is called a ``file_id``.  This is similar
to everything is a file in Linux.

To attempt to make paths easier to navigate, the download and upload methods include a ``folder``
and ``name`` attribute.  So if you wanted to upload a file in ``foo/bar/file.py``, you would set
``folder`` to ``foo/bar`` and ``name`` to ``file.py``.  You can omit the ``folder`` attribute
and the current directory will be used.  The motivation for this is to 1) make the file name and
save location explicit, and 2) standardize these variables accross the download and upload
functions.  When downloading a resource, you may want to keep the file name from the service,
or rename it.  By setting the ``name`` attribute to ``None``, the name of the resource will be
used.

"""

import logging
import mimetypes
from pathlib import Path
import shutil

_log = logging.getLogger(__name__)

class Storage(object):
    """
    .. _storage-class:

    The Storage class is designed to provide a standard interface for adding APIs that enable
    storage.  This class defines the basic required functions that must be implimented for two
    classes inheriting this class to work in the same workflow, assuming the correct API keys
    are used.  Switching storage objects should work seemlessly, if a Config object is used to
    initialize the Storage object.  If the API credentials are folderectly provided, this cannot
    be guarantied because different services had different methods of initialization.

    Different APIs might have different methods for identifying files.  For example, Box uses IDs
    for files and folders, but another service might use a path from the root directory.  The
    method of identifying files or folders is called a ``fid`` (file/folder identification) in
    DAPT.  Different implimentations might use different protocols for files and folders, so the
    Storage methods should take care of this.

    Required methods
    ----------------

    There are four required methods that all Storage objects must implement.  The required
    methods are download, delete, rename, and upload.  These methods are based off REST APIs,
    although the underlying implimentation do not need to use REST.
    """

    def download_file(self, file_id, folder='.', name=None, overwrite=True):
        """
        Download the file at the given file_id to the given path.

        Args:
            file_id (str): The file identification to be downloaded
            folder (str): The directory where the file should be saved
            name (str): The name that the file should be saved as.  If None is given (default),
            then the name of the file on the resource will be used.
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if successful and False otherwise
        """
        pass

    def download_folder(self, file_id, folder='.', name=None, overwrite=True):
        """
        Download the folder at the given file_id to the given path.

        Args:
            file_id (str): The folder identification to be downloaded
            folder (str): The directory where the file should be saved
            name (str): The name that the file should be saved as.  If None is given (default),
            then the name of the file on the resource will be used.
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if successful and False otherwise
        """
        pass

    def delete_file(self, file_id):
        """
        Delete the the given file.

        Args:
            file_id (str): The file identification to be downloaded

        Returns:
            True if successful and False otherwise
        """
        pass

    def delete_folder(self, file_id):
        """
        Delete the given folder.

        Args:
            file_id (str): The folder identification to be downloaded

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

    def rename_folder(self, file_id, name):
        """
        Rename the given folder.

        Args:
            file_id (str): The folder identification to be downloaded
            name (str): The new name of the file or folder

        Returns:
            True if the file or folder was renamed, False otherwise.
        """
        pass

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
        pass

    def upload_folder(self, file_id, name, folder='.', overwrite=True):
        """
        Upload a folder to the given folder.

        Args:
            file_id (str): The folder where the folder should be saved.
            name (str): The name that the file should be uploaded.
            folder (str): The directory where the file is stored.
            overwrite (bool): Should the data on your machine be overwritten.  True by default.

        Returns:
            True if the upload was successful and False otherwise.
        """
        pass

def check_overwrite_file(folder, name, overwrite, remove_existing):
    """
    This method checks to see if the file at the path specified should be overwritten.

    Args:
        folder (str): The directory where the file might be.
        name (str): The name of the file
        overwrite (bool): Should the file be overwritten
        remove_existing: (bool): Should the file be deleted if it already exists

    Returns:
        True if the file should be overwritten and False otherwise.
    """

    file_path = Path(folder) / name

    if file_path.exists():
        if overwrite:
            if remove_existing:
                file_path.unlink
                _log.info('Removing file %s' % file_path)
            return True
        else:
            return False

    return True

def check_overwrite_folder(folder, name, overwrite, make_folder):
    """
    This method checks to see if the file at the path specified should be overwritten.

    Args:
        folder (str): The directory where the file might be.
        name (str): The name of the folder
        overwrite (bool): Should the file be overwritten
        make_folder (bool): Should the directory be made if it passes the overwrite test.

    Returns:
        True if the folder can be overwritten and was created (if ``make_folder`` was True) and
        False otherwise.
    """

    folder = Path(folder)
    file_path = folder / name

    if file_path.exists() and not overwrite:
        return False

    if make_folder:
        parts = folder.parts
        parts_path = Path('')

        for part in parts:
            parts_path = parts_path / part

            if not parts_path.exists():
                parts_path.mkdir()

        if file_path.exists():
            shutil.rmtree(file_path)
        
        file_path.mkdir()

    return True

def get_mime_type(name):
    """
    Get the MIME type of the given file based on it's file extension.

    Args:
        name (str): the name of the file including the extension

    Returns:
        The MIME type of the file and None if the MIME type cannot be found.
    """

    return mimetypes.guess_type(name)[0]
