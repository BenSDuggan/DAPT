
__name__ = "dapt"
__version__ = "0.9.2"
__all__ = ['db', 'storage', 'config', 'param', 'tools']

import logging

from .config import Config
from .db import *
from .storage import *
from .param import Param
from .tools import *

# Temperatry loggin
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# add formatter to ch
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# add ch to logger
logger.addHandler(ch)
