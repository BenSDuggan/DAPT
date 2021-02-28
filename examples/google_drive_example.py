"""
Google Drive Example
====================

This is an example of how Google Drive can be used with DAPT.

In the example, a file and folder will be downloaded from a public Google Drive share.  The
content will then be uploaded to your Google Drive.  The content will be renamed on your Drive
and then deleted.  Between each step, the code will pause so you can see what changed.

You should change the ``config_path`` to the location of your config file.

"""

import os
import shutil

import dapt

# Change this
config_path = 'config.json'

google_drive_file_id = '19Eqo9gNyv1ORzIlAedQ3nqK9dq8jz2YQ'
google_drive_folder_id = '1YHP8a95vG6oFfKgpK_z6K-zNK-CxoNcc'

config = dapt.Config(path=config_path)
drive = dapt.storage.Google_Drive(config=config)

if drive.connect():
    print('Connected to Google Drive.')
else:
    print('There was an error connecting with Google Drive.')
    exit()

# Download file
print("Download file")
print(drive.download_file(file_id=google_drive_file_id))

# Download folder
print("Download folder")
print(drive.download_folder(file_id=google_drive_folder_id))

input('Check to see that the file and folder have been downloaded to your machine.')

# Upload file
print("Upload file")
print(drive.upload_file(file_id='root', name='ypsilon-lake-trail.jpg'))

# Upload folder
print("Upload folder")
print(drive.upload_folder(file_id='root', name='Colorado'))

input('Check to see that the file and folder have been uploaded to the root folder of your Drive.')

# Still need to implement

# Rename file

# Rename folder

# Delete file

# Delete folder

os.remove('ypsilon-lake-trail.jpg')
shutil.rmtree('Colorado')
