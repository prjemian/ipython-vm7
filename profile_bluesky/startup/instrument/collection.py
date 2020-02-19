
"""
configure for data collection
"""

from .session_logs import *
logger.info(__file__)

from .mpl import *

# are our soft IOCs running?
logger.info("check if soft IOCs are running")
from .iocs.check_iocs import *

logger.info("bluesky framework")

from .framework import *
from .devices import *
from .plans import *
from .utils import *

from apstools.utils import *

from .session_logs import logger
