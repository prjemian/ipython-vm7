
"""
simulators
"""

__all__ = []

from ..session_logs import logger
logger.info(__file__)


import apstools.devices
import numpy as np

from .calcs import calcs
from .motors import m1


apstools.devices.setup_lorentzian_swait(
    calcs.calc1,
    m1.user_readback,
    center = 2*np.random.random() - 1,
    width = 0.015 * np.random.random(),
    scale = 10000 * (9 + np.random.random()),
    noise=0.05,
)

try:
    from .my_registers import mover2, registers
    apstools.devices.setup_lorentzian_swait(
        calcs.calc2,
        mover2,
        center = 2*np.random.random() - 1,
        width = 0.015 * np.random.random(),
        scale = 10000 * (9 + np.random.random()),
        noise=0.05,
    )
    calcs.calc2.output_link_pv.put(registers.decimal1.pvname)
except NameError as exc:
    logger.warn(f"variable `registers` is not defined: {exc}")
