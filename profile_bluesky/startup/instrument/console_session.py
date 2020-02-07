
"""
configure for data collection in a console session
"""

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(__file__)

from .mpl.console import *

# from .logging_setup import *

# are our soft IOCs running?
from .iocs.check_iocs import *

logger.info("bluesky framework")

from .startup import *
from .devices import *
from .plans import *

from apstools.utils import show_ophyd_symbols, print_RE_md
