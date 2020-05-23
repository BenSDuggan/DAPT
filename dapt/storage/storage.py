"""
Storage
=======

The Storage class is designed to provide a standard interface for adding APIs that enable storage.  This class defines the basic required functions that must be implimented for two classes inheriting this class to work in the same workflow, assuming the correct API keys are used.  Switching storage objects should work seemlessly, if a Config object is used to initialize the Storage object.  If the API credentials are directly provided, this cannot be guarantied because different services had different methods of initialization.

Different APIs might have different methods for identifying files.  For example, Box uses IDs for files and folders, but another service might use a path from the root directory.  The method of identifying files or folders is called a ``fid`` (file/folder identification) in DAPT.  Different implimentations might use different protocols for files and folders, so the Storage methods should take care of this.

Required methods
----------------

There are four required methods that all Storage objects must implement.  The required methods are download, delete, rename, and upload.  These methods are based off REST APIs, although the underlying implimentation do not need to use REST.

"""

class Storage(object):
    """
    An interface to build similar Storage schemes for basic storage operations
    """

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
        pass

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