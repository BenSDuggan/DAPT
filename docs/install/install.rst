.. _install:

Install
=======

The easiest way to install DAPT is using pip.  To do so type:

``
pip install dapt
``

Alternatively, you can download a version the project.  It is recommended to download a `release <https://github.com/BenSDuggan/DAPT/releases>`_ of the project from GitHub for improved stability.  If you would like to download the most up to date version, then download the `repo <https://github.com/BenSDuggan/DAPT>`_ or clone it on your machine ``git clone https://github.com/BenSDuggan/DAPT``.  Once downloaded navigate to the root of the project (DAPT) and run ``pip install -r requirements.txt`` to install all of the dependencies.  If you use this method of installation, you will need to write all of your Python scripts using DAPT in the root directory of the project.  For these reasons, it's recommended to only use this method if would like to contribute to the project.

You can then test to make sure everything installed by starting a python session and then running:

```
import dapt
dapt.__version__
```
 
 You should see a version looking like ``0.9.*``.

 DAPT is maintained for Python >= 3.6 and a full list of requirements is given in `requirements.txt <https://github.com/BenSDuggan/DAPT/blob/dev/requirements.txt>`_

You can now use the library!  However, the functionality can be greatly increased by connecting some other services such as Google Sheets or Box.  See the below guides on how to include this functionality.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   sheets-install
   box-install