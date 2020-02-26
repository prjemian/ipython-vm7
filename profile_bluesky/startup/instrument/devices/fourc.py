

"""Four circle diffractometer (simulated)"""

__all__ = [
    "fourc",
    "fourc_example",
    "fourc_example_constraints",
    "fourc_example_plan",
    "lnolao",
]

from ..session_logs import logger
logger.info(__file__)

import gi
gi.require_version('Hkl', '5.0')
from hkl.diffract import E4CV, E4CH  #this works for mu=0
from hkl.util import Lattice

from bluesky import plans as bp
from bluesky import plan_stubs as bps

from ophyd import Component
from ophyd import PseudoSingle
from ophyd import SoftPositioner

from apstools.diffractometer import DiffractometerMixin


class FourCircleDiffractometer(DiffractometerMixin, E4CV):
    h = Component(PseudoSingle, '', labels=("hkl", "fourc"))
    k = Component(PseudoSingle, '', labels=("hkl", "fourc"))
    l = Component(PseudoSingle, '', labels=("hkl", "fourc"))

    omega = Component(SoftPositioner, labels=("motor", "fourc"))
    chi   = Component(SoftPositioner, labels=("motor", "fourc"))
    phi   = Component(SoftPositioner, labels=("motor", "fourc"))
    tth   = Component(SoftPositioner, labels=("motor", "fourc"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # since this diffractometer uses simulated motors,
        # prime the SoftPositioners (motors) with initial values
        # otherwise, position == None --> describe, etc gets borked
        for axis in (self.omega, self.phi, self.chi, self.tth):
            axis.move(0)


fourc = FourCircleDiffractometer('', name='fourc', labels=("diffractometer", "fourc"))
