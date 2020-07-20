# Changes starting from 

## New version

### General updates

* Adding logging to DAPT using Python's [logging](https://docs.python.org/3.8/library/logging.html) module
* Adding TravisCI testing for Python 3.9

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