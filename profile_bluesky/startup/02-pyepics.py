logger.info(__file__)
"""
ensure that PyEpics is available

Do this early in the setup so other setup can benefit.
"""

import epics

up = epics.caget("sky:UPTIME", timeout=1)
if up is None:
    logger.info("IOCs not running.  Starting them now...")
    start_ioc_script = "/home/mintadmin/bin/start_iocs.sh"
    os.system(start_ioc_script)
    logger.debug("IOCs started")
