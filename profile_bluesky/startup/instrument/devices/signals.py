
"""
"""

import apstools.devices
import logging
import numpy
from ophyd import EpicsSignalRO

from .calcs import calcs
from .motors import m1

logger = logging.getLogger(__name__)
logger.info(__file__)

shutter = apstools.devices.SimulatedApsPssShutterWithStatus(
    name="shutter", labels=("shutters",))
shutter.delay_s = 0.05 # shutter needs short recovery time after moving


# demo: use swait records to make "noisy" detector signals
noisy = EpicsSignalRO('sky:userCalc1', name='noisy', labels=("detectors",))


apstools.devices.setup_lorentzian_swait(
    calcs.calc1,
    m1.user_readback,
    center = 2*numpy.random.random() - 1,
    width = 0.015 * numpy.random.random(),
    scale = 10000 * (9 + numpy.random.random()),
    noise=0.05,
)

try:
    apstools.devices.setup_lorentzian_swait(
        calcs.calc2,
        mover2,
        center = 2*numpy.random.random() - 1,
        width = 0.015 * numpy.random.random(),
        scale = 10000 * (9 + numpy.random.random()),
        noise=0.05,
    )
    calcs.calc2.output_link_pv.put(registers.decimal1.pvname)
except NameError:
    logger.info("variable `registers` is not defined")
