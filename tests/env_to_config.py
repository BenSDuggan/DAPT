# Finds variables from the environment and creates a config file to use.  This is useful when using Travis CI as it allows API keys to be passed.

import os, sys, json, dapt

### Create initial config file
config = dapt.Config.create('test_config.json')

### Add Google Sheets API
config.config['sheets-creds-path'] = 'test_credentials.json'
google_creds = {
    "type":"service_account",
    "project_id":os.environ['GS_project_id'],
    "private_key_id":os.environ['GS_private_key_id'],
    "private_key":os.environ['GS_private_key'],
    "client_email":os.environ['GS_client_email'],
    "client_id":os.environ['GS_client_id'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url":os.environ['GS_client_x509_cert_url']
}

with open('test_config.json', 'w') as f:
    json.dump(google_creds, f)
