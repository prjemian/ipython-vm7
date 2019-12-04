logger.info(__file__)
"""
ensure that PyEpics is available

Do this early in the setup so other setup can benefit.
"""

import epics

up = epics.caget("sky:UPTIME", timeout=1)
if up is None:
    logger.info("IOCs not running.  Starting them now...")
    # ~/bin/start_iocs.sh
    start_ioc_script = "/home/mintadmin/bin/start_iocs.sh"
    # import subprocess
    # process = subprocess.Popen(
    #     start_ioc_script, 
    #     shell=True, stdout=subprocess.PIPE)
    # process.wait()
    # logger.debug(f"{process.returncode}")
    os.system(start_ioc_script)
    logger.debug("IOCs started")
