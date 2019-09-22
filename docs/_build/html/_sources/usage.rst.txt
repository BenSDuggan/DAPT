.. _usage:

Usage
=====

Once you have `installed <install.html>`_ DAPT and have verified that it's installed correctly you can start setting it up for usage.

Fields
------

Below are the fields that are used with parsing paramater sets.  Required paramaters are makred with an astrict(*).

+---------------------------+-----------------------------------------------------------------------------------------+
| Fields                    | Description                                                                             |
+===========================+=========================================================================================+
| **\*id (string)**         | Unique parameter set installed                                                          |
+---------------------------+-----------------------------------------------------------------------------------------+
| **\*status (string)**     | The current status of the paramater set. Blank values are unran (default),              |
|                           | ``success`` have finished and ``failed`` have failed.                                   |
+---------------------------+-----------------------------------------------------------------------------------------+
| **startTime (string)**    | The time that the paramater set began.  Times are in UTC time format.                   |
+---------------------------+-----------------------------------------------------------------------------------------+
| **endTime (string)**      | The time that the paramater set finished.  Times are in UTC time format.                |
+---------------------------+-----------------------------------------------------------------------------------------+
| **performedBy (string)**  | The username of the person that ran the paramater set.                                  |
+---------------------------+-----------------------------------------------------------------------------------------+
| **comments (string)**     | Any comments such as error messages relating to the paramater set.                      |
+---------------------------+-----------------------------------------------------------------------------------------+

