.. _index:

Distributed Automated Parameter Testing (DAPT)
==============================================


![Travis-CI](https://travis-ci.com/BenSDuggan/DAPT.svg?token=aV2WxyvqLfShpTx4gD3a&branch=master)
[![Documentation Status](https://readthedocs.org/projects/dapt/badge/?version=latest)](https://dapt.readthedocs.io/en/latest/?badge=latest)

A library to assist with running parameter sets across multiple systems.  The goal of this library is to provide a tool set and pipeline that make organizing, running and analyzing a large amount of parameter easier.  Some of the highlights include: 

* Provide an easy way to run paramater sets.
* Protocol for allowing teams to run parameter sets concurrently.
* Use Google Sheets as a database to host and manage paramater sets.
* Access to the Box API which allows files to be uploaded to box.

## Overview

When working on a project with or without access to high performance computing (HPC), there is often a need to perform large parameter sweeps.  Before developing DAPT, there were several problems the ECM team in Dr. Paul Macklin's research lab identified.  First, it was difficult to manage a large number of parameter sets with a large number of parameters.  Second, it would be nice to use Google Sheets to run the parameters for easier collaboration and management.  Third, only one person in the group would be running all the parameters, making their computer useless for the duration of the runs.  Finally, we needed to upload the data to Box for permanent storage and to allow the rest of the team to view the data.  

DAPT was written to solve these problems.  A "database" (CSV or Google Sheet) is used to store a list of parameter sets.  This database is managed by the `Param` class and provides methods to interact with and manage parameter sets.  the `Box` class allows data to be uploaded to [Box.com](https://box.com).  Sensitive API credentials can be stored in a config file (via the `Config` class) which can also be accessed by users to get other variables.

Future versions of the project will work to improve documentation, add examples, cleanup current functionality and add more features.  While most of the `dapt` module is documented, the intended way of using each method is not clearly explained.  There are examples given for the main features, however, again there is not a satisfactory amount of documentation.  Some of the exciting new features to come will be notification and logging integration.  For example, we would like to add Slack notification so teams can be notified if there is an error with a test.




### Dependencies
**Python:** >=3.6

All dependences are located in [requirements.txt](requirements.txt).



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install/install
   usage
   examples/examples
   code/dapt