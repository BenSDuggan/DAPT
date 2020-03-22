# Paper

Directory containing the paper and the tools to build it.

## Install prereq

### Linux

`sudo apt-get install texlive-latex-extra texlive-bibtex-extra biber cm-super`

### MacOS

- `brew install pandoc`
- `brew install pandoc-citeproc`
- `brew install mactex`


## Make file rules
```
make			# Default behavior (generate latex)
make pdf		# Make latex and compile it
make clean		# Clean up generated files
```

