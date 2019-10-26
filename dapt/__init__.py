"""

Distributed Automated Paramater Testing (DAPT)
==============================================

This is __init__.py
"""

__version__ = "0.8.2"

import sys, argparse
from . import config

parser = argparse.ArgumentParser(description='Distributed Automated Parameter Testing (DAPT)\nA library to assist with running parameter sets across multiple systems.', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--f', metavar='config.json', default='config.json', type=str, action='store', help="The path to the config file.")
parser.add_argument('--l', action='store_true', help="Reset the value of \'last-test\' to None.")
parser.add_argument('--c', action='store_true', help="Create a blank config file.")
parser.add_argument('--s', action='store_true', help="Remove keys from the config file so it can be made public.")

args = parser.parse_args()
if args.l:
    # Remove last-test from config file
    conf = config.Config(args.f)
    conf.config['last-test'] = None
    conf.update_config()
if args.c:
    # Reset config file
    config.Config.create(args.f)
if args.s:
    # Safe config file
    config.Config.safe(args.f)

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