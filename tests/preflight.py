"""
Things that should be setup before starting anything in the testing pipeline.
"""

import os

os.environ['DAPT_config_path'] = 'test_config.json'
os.environ['GS_creds_path'] = 'test_credentials.json'