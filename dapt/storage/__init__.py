"""

.. _storage:

Storage Overview
================

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



from .base import Storage
from .box import Box
from .google_drive import Google_Drive
