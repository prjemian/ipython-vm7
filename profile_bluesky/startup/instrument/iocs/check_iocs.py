
"""
check that our EPICS soft IOCs are running
"""

import epics
import os

from ..session_logs import logger
logger.info(__file__)

up = epics.caget("sky:UPTIME", timeout=1)
if up is None:
    logger.info("EPICS sky IOCs not running.  Starting them now...")
    start_ioc_script = "/home/mintadmin/bin/start_iocs.sh"
    os.system(start_ioc_script)
    logger.debug("sky IOCs started")
else:
    logger.info("EPICS sky IOCs ready...")

# up = epics.caget("IOC:float1.NAME", timeout=1)
# if up is None:
#     logger.info("EPICS registers IOC not running.  Starting now...")
#     path = os.path.join(os.path.dirname(__file__), "..", "..")
#     start_ioc_script = os.path.join(
#         os.path.abspath(path), 
#         "epics-soft-ioc", "in_screen.sh")
#     r = os.system(start_ioc_script)
#     logger.debug(f"registers IOC started: {r}")
# else:
#     logger.info("EPICS registers IOC ready...")
