"""

.. _database:

Database Overview
=================

Databases are the places where parameter spaces live.  You must use a database in DAPT and the
:ref:`Param class <param>` requires one to be provided.  DAPT views databases similarly to a
spreedsheet.  Databases can be local or remote.  If a database is local
(e.g. :ref:`delimited-file`), then only one person can run the parameters.  When a remote database
(e.g. :ref:`google-sheets`) is used, then multiple people can run the tests simultaneously.

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

.. _database-schematic:

Schematic
---------

The database is made up of tables, identified by a key (``str`` or ``int``), which contain columns
and rows.  The tables of database hold a parameter space and each row is a parameter set.  A
column contains particular fields (attributes) within the space.  The column names are called
fields and should be strings.  Rows are identified by an index, similar to a list.  The indexing
starts from zero and increments.

Cell holds the value of a particular row and column.  Currently, all cells are concidered strings,
however, some databases allow for other types to be inserted, or automatically inference the type.
For this reason, you might need to cast cells to different type.

.. _database-config:

Config
------

It is recommend to use a :ref:`config` with the database classes.  While all classes can be 
instantiated without a ``Config``,  using one greatly increases useability and simplifies
switching between databases.  Each database has a reserved ``Config`` key (listed below).  The
value will be a dictionary with API credentials and database settings.  The the structure of
configuration is similar between databases, but specific to the API connection requirements.
Specific database classes have more information on required configuration contents.

+---------------------------+----------------------------------------------------------------+
| Fields                    | Description                                                    |
+===========================+================================================================+
| ``delimited-file`` (str)  | Reserved word for ``Delimited_file`` database.                 |
+---------------------------+----------------------------------------------------------------+
| ``sheets`` (str)          | Reserved word for ``Sheets`` database.                         |
+---------------------------+----------------------------------------------------------------+

.. _database-usage:

Usage
-----

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
the dictionary are fields and values are specific cells in the table.  The fields of the table
can be retrieved using the ``fields()`` method.

    >>> db.fields()
    ['id', 'start-time', 'status', 'a', 'b', 'c']

A specific cell can be changed using the ``update_cell()`` method.  This method requires the row
index (starting from 0), field, and updated value.  For example, we can update field c with id
"t2" to 20.

    >>> db.update_cell(1, 'c', 20)
    True

An entire row can be updated with the ``update_row()`` method.  This method only requires the
row index (starting from 0) and the updated row (given as a dictionary).

    >>> db.update_row(1, {'id':'t2', 'start-time':'2019-09-06 17:37',
    'end-time':'2019-09-06 17:55', 'status':'finished', 'a':'10', 'b':'10', 'c':'20'})
    [{'id':'t1', 'start-time':'2019-09-06 17:23', 'end-time':'2019-09-06 17:36',
    'status':'finished', 'a':'2', 'b':'4', 'c':'6'},
	{'id':'t2', 'start-time':'2019-09-06 17:37', 'end-time':'2019-09-06 17:55',
    'status':'finished', 'a':'10', 'b':'10', 'c':'20'},
	{'id':'t3', 'start-time':'', 'end-time':'', 'status':'', 'a':'10', 'b':'-10', 'c':''}]

"""


from .base import Database
from .delimited_file import Delimited_file
from .sheets import Sheet


