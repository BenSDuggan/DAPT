"""

.. _database:

Databases are the places where parameter spaces live.  You must use a database in DAPT and the
:ref:`Param class <param>` requires one to be provided.  DAPT views databases similarly to a
spreedsheet.  Databases can be local or remote.  If a database is local
(e.g. :ref:`delimited-file`), then only one person can run the parameters.  When a remote database
(e.g. :ref:`google-sheets`) is used, then multiple people can run the tests simultaneously.

Each database can contain several tables, which contain columns and rows.  The tables of database
hold a parameter space and each row is a parameter set.  A column contains particular attributes
within the space.  

The databases provided in DAPT are all built off of the :ref:`base-database`.  This ensures that
databases can be interchanged easily.  For example, if you were using the :ref:`delimited-file`
database, you could provide the :ref:`google-sheets` to the :ref:`Param class <param>` instead.  
This works because all databases must support the same core functions within the
:ref:`base-database` class.  Some databases may have additional methods which work better with
its design.

The only difference between these classes, from the user level, is the ``init`` and  ``connect()``
methods.  Database classes can be initialized using only a :ref:`config` class.  This makes it
easy to swap between and initialize databases.  Because some databases required users to login,
you must connect to it before it can be accessed.  This should be done before trying to access
the data.

.. _database-usage:

Usage
^^^^^

Because the usage for each database is almost identical, it will be explained here instead of in
the submodules.  More explications on the methods, checkout the :ref:`base-database`.  The
connection steps for each database will be explained within the respective documentation.

For this example, the :ref:`Sample database <sample-db>` will be used.  By calling the
``sample_db()`` method, an example :ref:`delimited-file` class is created.

    >>> db = dapt.tools.sample_db(file_name='sample_db.csv', delimiter=',')

This method returns an instance of the database, but the line below shows how a new database
instance can be created.

    >>> db = dapt.db.Delimited_file(path='sample_db.csv', delimiter=',')

The :ref:`delimited-file` class doesn't need to connect to anything, but most databases will
so you should always run ``connect()``.

    >>> db.connect()
    True

The table can simply be viewed by running:

    >>> db.get_table()
    [{'id': 't1', 'start-time': '2019-09-06 17:23', 'end-time': '2019-09-06 17:36',
      'status': 'finished', 'a': '2', 'b': '4', 'c': '6'}, 
    {'id': 't2', 'start-time': '', 'end-time': '', 'status': '', 'a': '10', 'b': '10', 'c': ''},
    {'id': 't3', 'start-time': '', 'end-time': '', 'status': '', 'a': '10', 'b': '-10', 'c': ''}]

Tables are represented as an array of dictionaries.  Each element is a parameter set.  The keys in
the dictionary are attributes and values are specific cells in the table.

"""


from .base import Database
from .delimited_file import Delimited_file
from .sheets import Sheet


