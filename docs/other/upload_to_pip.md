# Upload to PIP

## To upload a file to pip:

`python3 setup.py sdist bdist_wheel`

`python3 -m twine upload dist/*`

## To clean up files

`sudo rm -r dapt.egg-info/ build dist`