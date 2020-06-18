# docs

This folder contains the documentation for DAPT.  The documentation is done using Sphinx.

## Install

Assuming you have python installed, install sphinx by running `pip install -U sphinx`.  Next you need to install the sphinx theme by running `pip install sphinx_rtd_theme`.

## Compile

1. Run `sphinx-apidoc -o modules/ ../dapt`
2. Run `sphinx-build -b html . _build/`

To make the PDF documentation you will need to have pdflatex installed.  You can then compile it by running `sphinx-build -M latexpdf . _build/`.
