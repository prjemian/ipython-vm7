
import apstools.synApps
from ophyd import EpicsSignalRO
import logging

logger = logging.getLogger(__name__)
logger.info(__file__)

calcs = apstools.synApps.UserCalcsDevice("sky:", name="calcs")
calcouts = apstools.synApps.UserCalcoutDevice("sky:", name="calcouts")

calcs.enable.put(1)
