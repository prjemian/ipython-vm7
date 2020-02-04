
"""
configure for data collection in a console session
"""

import logging

print("prechecks")
from .check_python import *
from .check_bluesky import *

from .logging_setup import *
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(__file__)

# are our soft IOCs running?
from .check_iocs import *

logger.info("bluesky framework")
from .mpl_setup import *

from .framework import *
from .user_dir import *
from .metadata import *
from .callbacks import *

from ..devices import *
from ..plans import *

from apstools.utils import show_ophyd_symbols, print_RE_md
