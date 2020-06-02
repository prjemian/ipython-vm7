
"""
simulators
"""

__all__ = []

from ..session_logs import logger
logger.info(__file__)


import apstools.devices
import numpy as np

from .calcs import calcs
from .motors import m1, m2


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

# demonstrate a grid scan: noisy2d(m1, m2)
#   RE(bp.grid_scan([noisy2d], m1, -0.5, 0.5, 7,  m2, -1, 1, 11, True))
calcs.calc3.reset()
calcs.calc3.scanning_rate.put("Passive")
calcs.calc3.description.put("2-D mesh (m1, m2)")
calcs.calc3.channels.A.input_pv.put(m1.user_readback.pvname)
calcs.calc3.channels.B.input_pv.put(m2.user_readback.pvname)
calcs.calc3.channels.C.input_value.put(10000 * (9 + np.random.random()))
# calcs.calc3.channels.D.input_value.put()
# calcs.calc3.channels.E.input_value.put()
# calcs.calc3.channels.F.input_value.put()
# calcs.calc3.channels.G.input_value.put()
# calcs.calc3.channels.H.input_value.put()
# calcs.calc3.channels.I.input_value.put()
# calcs.calc3.channels.J.input_value.put()
# calcs.calc3.channels.K.input_value.put()
# calcs.calc3.channels.L.input_value.put()
calcs.calc3.calculation.put("C * RNDM")
calcs.calc3.precision.put(2) 
calcs.calc3.scanning_rate.put("I/O Intr")
noisy2d = calcs.calc3.calculated_value
