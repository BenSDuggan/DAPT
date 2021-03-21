# Change log 

## New version (0.9.3)

### Tests

* Added `--test_creds`, `--test_login`, and `--all` that let you exclude tests requiring API credentials or logging in.
* Added testing classes for DB and storage to make it easier to add tests for APIs.

### Database

* Added `fields` method and deprecated the `get_keys()` method.  Will remove `get_keys()` in version 0.9.5.
* No longer returning `OrderedDict` as it doesn't really matter if dictionary is ordered.
* Ensuring `Delimited_file` and `Sheets` have working `connect()` and `connected()` methods.

### db.Sheets

* Change authentication model to use `google.oauth2.service_account` from `oauth2client.service_account`

### db.Delimited_file

* Updating documentation
* Using key-word arguments now
* Added support for config

## 0.9.2

### General updates

* Adding logging to DAPT using Python's [logging](https://docs.python.org/3.8/library/logging.html) module
* Adding TravisCI testing for Python 3.9

### Storage

* Added `check_overwrite_file()` and `check_overwrite_folder()` functions to standardize the overwriting function of files and folders.
### Documentation

* Improved the organization of documentation

## 0.9.1.4

### General updates

* Moved database code to new `dapt.db` (database) module to better organize the code.

### Config

* Added `config.get_values()` method that gets the value from the config given a key.  This can be done recursively and also by giving a path to the value (by giving each key in a list).
* Adding optional keys `remove-zip` and `remove-movie`.  This is used by `tools.data_cleanup()`.
* Added helper function `_find_value` for recursively finding values.
* Made all Google Sheets variables be `sheets-*`.  Most of the Sheets variables were just `sheet-*`.
* Make config act like a dictionary so `config.config` doesn't need to be called.

### db.Sheets

* Made sure that Google Sheets is indexed from 0.
* Move Sheets to db folder

### db.Delimited_file

* Moved `Delimited_file` to new `dapt.db` module

### storage.Box

* Box has been moved to the storage module.
* Box now uses standard methods (defined in storage) and can upload, download, rename, and delete.
* Improving Config integration so it is cleaner.  Attributes are now stored in a dictionary inside the "box" key.

### Tools

* Added documentation to the `tools` module
* Made all functions use underscores instead of camelCase.
* Changed param settings file output (`autoParamSettings.txt`) to `dapt_param_settings.txt`.

### Examples

* Moving PhysiCell example to its own repo
* Fixed Google Sheets example so that it is indexed from 0

### Tests

* Fixed Google Sheet names in Config file
* Fixed Sheets tests so that they test for indexing at 0.
* Changed Sheets and Delimited_file so that they work with the new module