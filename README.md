# Distributed Automated Parameter Testing (DAPT)

![Travis-CI](https://travis-ci.com/BenSDuggan/DAPT.svg?token=aV2WxyvqLfShpTx4gD3a&branch=master)

A library to assist with running parameter sets across multiple systems.

## Overview
ToDo

## Install

To install dowload the [repo](https://github.com/BenSDuggan/DAPT) or clone it on your machine `git clone https://github.com/BenSDuggan/DAPT`.  Once downloaded navigate to the root of the project (DAPT) and run `pip install -r requirements.txt` to install all of the dependences.  You can then test to make sure everything installed by starting a python session and then running:
```
import dapt
dapt.__version__
```

### Dependencies
**Python:** >=3.5
All dependences are located in [requirements.txt](requirements.txt).
****

## Documentation
Documentation is done using [Sphinx](http://www.sphinx-doc.org/en/master/).  The [docs](/docs) folder holds all of the resources to document the code.  Here is a good tutorial on Sphinx if your not familiar <https://medium.com/@eikonomega/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365>.  Google docstrings are used for inline commenting inside each file.

To build docs only your local machine simply type `make html` inside the [docs](/docs) folder.


## Example usage
ToDo

## Contribute
ToDo

## Project structure
```
.
├── dapt                 			# The folder where the DAPT library is housed
├── docs             				# Documentation for project
└── examples          				# Python scripts showing how to use the program
```

## Unit tests
Unit tests are ran using [Pytest](pytest.org).  You can install it by running `pip install -U pytest`.  The tests are located in the `tests` folder inside of the `DAPT` module.  The tests can be run by opening a python session and then running:
```
import dapt
dapt.test()
```

or by running `pytest` in the main project directory.

For more information on the tests go to the [`tests`](dapt/tests) folder.

