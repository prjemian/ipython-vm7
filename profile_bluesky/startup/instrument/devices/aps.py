
"""
APS only: connect with facility information
"""

import apstools.devices
import logging
from ..startup.framework import sd

logger = logging.getLogger(__name__)
logger.info(__file__)

aps = apstools.devices.ApsMachineParametersDevice(name="aps")
sd.baseline.append(aps)

undulator = apstools.devices.ApsUndulatorDual("ID45", name="undulator")
sd.baseline.append(undulator)
