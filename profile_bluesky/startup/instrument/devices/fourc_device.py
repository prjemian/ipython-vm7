"""Four circle diffractometer (simulated)"""

__all__ = [
    "fourc",
]

from ..session_logs import logger

logger.info(__file__)

import gi

gi.require_version("Hkl", "5.0")

from apstools.diffractometer import DiffractometerMixin
from bluesky import plan_stubs as bps
from bluesky import plans as bp
from hkl.diffract import E4CV
from hkl.util import Lattice
from ophyd import Component
from ophyd import PseudoSingle
from ophyd import SoftPositioner


class FourCircleDiffractometer(DiffractometerMixin, E4CV):
    h = Component(PseudoSingle, "", labels=("hkl", "fourc"), kind="hinted")
    k = Component(PseudoSingle, "", labels=("hkl", "fourc"), kind="hinted")
    l = Component(PseudoSingle, "", labels=("hkl", "fourc"), kind="hinted")

    omega = Component(SoftPositioner, labels=("motor", "fourc"), kind="hinted")
    chi = Component(SoftPositioner, labels=("motor", "fourc"), kind="hinted")
    phi = Component(SoftPositioner, labels=("motor", "fourc"), kind="hinted")
    tth = Component(SoftPositioner, labels=("motor", "fourc"), kind="hinted")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # since this diffractometer uses simulated motors,
        # prime the SoftPositioners (motors) with initial values
        # otherwise, position == None --> describe, etc gets borked
        for axis in (self.omega, self.phi, self.chi, self.tth):
            axis.move(0)


fourc = FourCircleDiffractometer("", name="fourc", labels=("diffractometer", "fourc"))
