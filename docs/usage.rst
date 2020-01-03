.. _usage:

Usage
=====

Once you have `installed <install.html>`_ DAPT and have verified that it's installed correctly you can start setting it up for actual parameter runs.  There are several ways to run DAPT but the basic philosophy is outlined below.  You can also look at specific `examples <https://github.com/BenSDuggan/DAPT/examples>`_.  To use DAPT, start by importing it.

.. code-block:: python

    import dapt

DAPT can be run with or without a configuration file.  The code is easier to use with a config file but it is not strictly necessary.  If you would like to create a config file, you should consult the `Config <https://dapt.readthedocs.io/en/latest/code/config.html>`_ class documentation.  Assuming you have created a config file called ``config.json``, you can create a Config object.

.. code-block:: python

    config = dapt.Config(path='config.json')

Next, you need to pick a `Database <https://dapt.readthedocs.io/en/latest/code/database.html>`_.  A Database is a class that allows you get access a list of parameter sets.  There are currently two Databases: a `Delimited file <https://dapt.readthedocs.io/en/latest/code/delimited_file.html>`_ and `Google sheets <https://dapt.readthedocs.io/en/latest/code/sheet.html>`_.  Below shows how to create the database objects.

.. code-block:: python

    db = data.Delimited_file('csv_file.csv', delimiter=',') # Create a Delimited file DB
    # or
    db = data.Sheet(config=config) # Create a Sheet DB with a config file
    # or
    spreedsheet_id = 'xxxxxx' # Google Sheet spreedsheet id
    creds = 'credentials.json' # Path to Google Sheets API credentials
    db = data.Sheet(spreedsheet_id=spreedsheet_id, creds=creds) # Create a Sheet DB with a config file

Now you can create the `Param <https://dapt.readthedocs.io/en/latest/code/param.html>`_ object to start processing parameters.  Create a Param object with the code below.

.. code-block:: python

    param = dapt.Param(db, config=config)

You can now use the methods in the Param class to get the next parameter set and manage the parameter set.

