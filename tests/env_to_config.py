# Finds variables from the environment and creates a config file to use.  
# This is useful when using Travis CI as it allows API keys to be passed.

import os
import json

import preflight

### Create initial config file
config = {"last-test":None, "user-name":None, "spreedsheet-id":None, "sheets-creds-path":None, "sheet-worksheet-id":None, "sheet-worksheet-title":None, "client-id":None, "client-secret":None, "box-folder-id":None, "reset-time":None, "num-of-runs":None, "computer-strength":None, "access-token":None, "refresh-token":None}
config['sheets-creds-path'] = 'test_credentials.json'
config['sheets-worksheet-title'] = 'daptTest'
config['sheets-spreedsheet-id'] = '1gIhv8Vfm01Hsjcqhukl6t8pX-wRJ1PVzwmwY4bezieg'

with open(os.environ['DAPT_config_path'], 'w') as f:
    json.dump(config, f)

### Add Google Sheets API
# Get the escaped credentials -> descape & make dict -> export as JSON
google_creds = json.loads(str(os.environ['GS_creds']))

with open(os.environ['GS_creds_path'], 'w') as f:
    json.dump(google_creds, f)
