# Test logging stuff

import dapt, logging


logger = logging.getLogger('sample logger')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# add formatter to ch
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# add ch to logger
logger.addHandler(ch)

logger.warning('sup')

db = dapt.tools.sample_db()
param = dapt.Param(db)

params = param.next_parameters()



