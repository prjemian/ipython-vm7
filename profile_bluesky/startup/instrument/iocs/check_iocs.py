
"""
check that our EPICS soft IOCs are running
"""

from ..session_logs import logger
logger.info(__file__)

import epics
import os
import subprocess


def run_command(command):
    with subprocess.Popen(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
    ) as process:
        outs, errs = process.communicate()
        if len(outs.strip()) > 0:
            logger.info(outs.strip().decode())
        if len(errs.strip()) > 0:
            logger.error(errs.strip().decode())


up = epics.caget("sky:UPTIME", timeout=1)
if up is None:
    logger.info("EPICS sky IOCs not running.  Starting them now...")
    run_command("/home/mintadmin/bin/start_iocs.sh")
    logger.debug("sky IOCs started")
else:
    logger.info("EPICS sky IOCs ready...")

up = epics.caget("IOC:float1.NAME", timeout=1)
if up is None:
    logger.info("EPICS registers IOC not running.  Starting now...")
    path = os.path.abspath(os.path.dirname(__file__))
    run_command(os.path.join(path, "in_screen.sh"))
    logger.debug(f"registers IOC started")
    run_command("screen -ls".split())
else:
    logger.info("EPICS registers IOC ready...")
