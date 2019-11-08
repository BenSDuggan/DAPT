# Distributed Automated Parameter Testing (DAPT)

![Travis-CI](https://travis-ci.com/BenSDuggan/DAPT.svg?token=aV2WxyvqLfShpTx4gD3a&branch=master)

A library to assist with running parameter sets across multiple systems.  The goal of this library is to provide a tool set and pipeline that make organizing, running and analyzing a large amount of parameter easier.  Some of the highlights include: 

* Provide an easy way to run paramater sets.
* Protocol for allowing teams to run parameter sets concurrently.
* Use Google Sheets as a database to host and manage paramater sets.
* Access to the Box API which allows files to be uploaded to box.

## Overview

When working on a project with or without access to high performance computing (HPC), there is often a need to perform large parameter sweeps.  Before developing DAPT, there were several problems the ECM team in Dr. Paul Macklin's research lab identified.  First, it was difficult to manage a large number of parameter sets with a large number of parameters.  Second, it would be nice to use Google Sheets to run the parameters for easier collaboration and management.  Third, only one person in the group would be running all the parameters, making their computer useless for the duration of the runs.  Finally, we needed to upload the data to Box for permanent storage and to allow the rest of the team to view the data.  

Making the dream come true.

Next steps.


## Install

The easiest way to install DAPT is using pip.  To do so type:
```
pip install dapt
```

Alternatively, you can dowload the project.  It is recommended to download a [release](https://github.com/BenSDuggan/DAPT/releases) of the project from GitHub for improved stability.  If you would like to download the most up to date version, then download the [repo](https://github.com/BenSDuggan/DAPT) or clone it on your machine `git clone https://github.com/BenSDuggan/DAPT`.  Once downloaded navigate to the root of the project (DAPT) and run `pip install -r requirements.txt` to install all of the dependences.  If you use this method of installation, you will need to write all of your Python scripts using DAPT in the root directory of the project.  For these reasons, it's recommended to only use this method if would like to contribute to the project.

You can then test to make sure everything installed by starting a python session and then running:
```
import dapt
dapt.__version__
```

You should see ***0.9.0***.

### Dependencies
**Python:** >=3.5
All dependences are located in [requirements.txt](requirements.txt).


## Documentation
You can view the most recent documentation on RTD [here]().  Documentation is performed using [Sphinx](http://www.sphinx-doc.org/en/master/).  The [docs](/docs) folder holds all of the resources to document the code.  Here is a good [tutorial](https://medium.com/@eikonomega/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365) on Sphinx if your not familiar with it.  Google docstrings are used for inline commenting inside each file.

To build docs on your local machine simply type `make html` inside the [docs](/docs) folder.


## Example usage
Examples of some basic uses of DAPT are located in the [examples](/examples) folder.  Before running any of the tests, ensure that you have installed DAPT.  If you just downloaded the repo and did not install using `pip` then move the tests into the root of the directory (i.e. [DAPT/](/)).  This step is necessary to ensure that `dapt` can properly be imported.


## Contribute
If you would like to contribute please fork the repo and make a pull request explaining what you added/fixed and why you added it.  If you are adding a new feature please write a unit test for it.  For more information on unit tests see the [test](/tests) folder.

### Project structure
```
.
├── dapt                 			# The folder where the DAPT library is housed
├── docs             				# Documentation for project
├── examples          				# Python scripts showing how to use the program
└── tests           				# Unit tests for DAPT
```

### Unit tests
Unit tests are ran using [Pytest](pytest.org).  You can install it by running `pip install -U pytest`.  The tests are located in the `tests` folder inside of the `DAPT` module.  The tests can be run by opening a python session and then running:
```
import dapt
dapt.test()
```

or by running `pytest` in the main project directory.

For more information on the tests go to the [tests](dapt/tests) folder.

