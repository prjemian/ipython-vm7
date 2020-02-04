
"""
aliases & imports for bluesky modules
"""

# convenience imports
from bluesky.callbacks import *
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from time import sleep
import numpy as np
import bluesky.magics


# Uncomment the following lines to turn on 
# verbose messages for debugging.
# ophyd.logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)


# diagnostics
from bluesky.utils import ts_msg_hook
#RE.msg_hook = ts_msg_hook
from bluesky.simulators import summarize_plan
