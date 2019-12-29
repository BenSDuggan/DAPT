# Release Notes

## Next version

### Config

* Added `config.get_values()` method that gets the value from the config given a key.  This can be done recursively and also by giving a path to the value (by giving each key in a list).
* Adding optional keys `remove-zip` and `remove-movie`.  This is used by `tools.data_cleanup()`.
* Added helper function `_find_value` for recursively finding values.

### Tools

* Added documentation to the `tools` module
* Made all functions use underscores instead of camelCase.
* Changed param settings file output (`autoParamSettings.txt`) to `dapt_param_settings.txt`.

### Examples

* Added PhysiCell example
