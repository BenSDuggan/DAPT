# Distributed Automated Parameter (DAP) Testing

## Install
To install dowload the [repo](https://github.com/BenSDuggan/DAPT) or clone it on your machine `git clone https://github.com/BenSDuggan/DAPT`.  Once downloaded navigate to the root of the project (DAPT) and run `pip install -r requirements.txt` to install all of the dependences.  You can then test to make sure everything installed by starting a python session and then running:
```
import dap
dap.__version__
```

## Project structure
```
.
├── dap                 			# The folder where the DAP library is housed
├── docs             				# Documentation for project
├── examples          				# Python scripts showing how to use the program
└── tests                  			# Test cases
```

## Documentation
Documentation is done using [Sphinx](http://www.sphinx-doc.org/en/master/).  This allows for easy automatic documentation.  The *docs* folder holds all of the resources to document the code.  Here is a good tutorial on Sphinx if your not familiar <https://medium.com/@eikonomega/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365>.  Google docstrings are used for inline commenting inside each file.

## Unit tests
Unit tests are ran using [Pytest](pytest.org).  You can install it by running `pip install -U pytest`.  The tests are located in the `tests` folder inside of the `DAP` module.  The tests can be run by opening a python session and then running:
```
import dap
dap.test()
```
For more information on the tests go to the [`tests`](dap/tests) folder.