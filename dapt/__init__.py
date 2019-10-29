"""

Distributed Automated Paramater Testing (DAPT)
==============================================

This is __init__.py
"""

name = "dapt"
__version__ = "0.9.0"

import sys, argparse
from . import config

parser = argparse.ArgumentParser(description='Distributed Automated Parameter Testing (DAPT)\nA library to assist with running parameter sets across multiple systems.', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--f', metavar='config.json', default='config.json', type=str, action='store', help="The path to the config file.")
parser.add_argument('--r', action='store_true', help="Reset the config file.  \'last-test\':None")
parser.add_argument('--c', action='store_true', help="Create a blank config file.")
parser.add_argument('--s', action='store_true', help="Remove keys from the config file so it can be made public.")

args = parser.parse_args()
if args.r:
    # Remove last-test from config file
    conf = config.Config(args.f)
    if conf.config['last-test']:
        conf.config['last-test'] = None
    #if conf.config['performed-by']:
    #    conf.config['performed-by'] = None
    conf.update_config()
    exit()
if args.c:
    # Reset config file
    config.Config.create(args.f)
    exit()
if args.s:
    # Safe config file
    config.Config.safe(args.f)
    exit()

from . import box
from . import database
from . import delimited_file
from . import sheets
from . import param
from . import tools

def test():
    from . import tests
    import pytest

    pytest.main()