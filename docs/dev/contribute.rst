.. _contribute:

Contribute
==========

If you would like to contribute please fork the repo and make a pull request explaining what you added/fixed and why you added it.  When you write a new feature please write tests in the ``test`` directory and documentation in the ``docs`` folder.

Documentation
-------------

Documentation is performed using `Sphinx <http://www.sphinx-doc.org/en/master/>`_.  The docs folder holds all of the resources to document the code.  If you're not familiar with Sphinx you can read this `Medium tutorial <https://medium.com/@eikonomega/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365>`_ for an introduction.  Google docstrings are used for inline commenting inside each file.

You can compile the docs by running ``make build-html``, assuming you have sphinx installed.  This will remove the old documentation and create the new html documentation in ``docs/_build/html``.


Tests
-----

Tests are located in the `tests <https://github.com/BenSDuggan/DAPT/tests>`_ folder and written using `pytest <https://docs.pytest.org/en/latest/>`_.  You can run the tests locally by running ``python3 -m pytest`` in the root DAPT directory.  This assumes that you have a configuration file named ``test_config.json`` in the root directory.  The convention used is to name all files and functions in the test directory ``test_x``, where x is the name/description of the test.

