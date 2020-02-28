
"""kappa diffractometer (simulated)"""

__all__ = [
    "kappa",
    # "kappa_example",
    # "kappa_example_constraints",
    "kappa_example_plan",
]

from ..session_logs import logger
logger.info(__file__)

import collections
import gi
gi.require_version('Hkl', '5.0')
from hkl.diffract import K4CV
from hkl.util import Lattice

from bluesky import plans as bp
from bluesky import plan_stubs as bps

from ophyd import Component
from ophyd import EpicsMotor
from ophyd import PseudoSingle
from ophyd import SoftPositioner

from apstools.diffractometer import Constraints, DiffractometerMixin

# from .scaler import I0Mon, diode, scint


# for more configuration ideas, see
# https://github.com/prjemian/ipython_poof/blob/23db4dd2b00b780a9f021953f4bbf43bfdb78aa6/profile_bluesky/startup/16-tardis.py

class KappaDiffractometer(DiffractometerMixin, K4CV):
    h = Component(PseudoSingle, '', labels=("hkl", "kappa"))
    k = Component(PseudoSingle, '', labels=("hkl", "kappa"))
    l = Component(PseudoSingle, '', labels=("hkl", "kappa"))

    # energy : Signal unless we override it here
    komega = Component(SoftPositioner, labels=("motor", "kappa"))
    kappa  = Component(SoftPositioner, labels=("motor", "kappa"))
    kphi   = Component(SoftPositioner, labels=("motor", "kappa"))
    tth    = Component(SoftPositioner, labels=("motor", "kappa"))

    # omega =   Component(SoftPositioner)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # since this diffractometer uses simulated motors,
        # prime the SoftPositioners (motors) with initial values
        # otherwise, position == None --> describe, etc gets borked
        for axis in (self.komega, self.kappa, self.kphi, self.tth):
            axis.move(0)

kappa = KappaDiffractometer('', name='kappa', labels=("diffractometer", "kappa"))
kappa.calc.engine.mode = kappa.engine.modes[0]

logger.info(f"{kappa.name} modes: {kappa.engine.modes}")
logger.info(f"selected mode: {kappa.calc.engine.mode}")

# define some constraints in a dictionary
diffractometer_constraints = {
    # axis: AxisConstraints(lo_limit, hi_limit, value, fit)
    "kappa": AxisConstraints(-10, 87, 0, True),
    "tth": AxisConstraints(-91, 91, 0, True),
    
    # we don't have these axes. Fix them to 0
    "kphi": AxisConstraints(0, 0, 0, False),
    "komega": AxisConstraints(0, 0, 0, False),    #kappa.omega.position.real
    
    # # Attention naming convention inverted at the detector stages!
    # "delta": AxisConstraints(-5, 180, 0, True),
    # "gamma": AxisConstraints(-5, 180, 0, True),
}

kappa.applyConstraints(diffractometer_constraints)
kappa.showConstraints()

# define a crystal by its lattice
kappa.calc.new_sample('cubic_sample', 
        lattice=Lattice(
            a=5.14, b=5.14, c=5.14, 
            alpha=90, beta=90, gamma=90))

# calculate using the default UB matrix

logger.info(kappa.forwardSolutionsTable([(1, 0, 0)]))
kappa.resetConstraints()
kappa.showConstraints()
logger.info(kappa.forwardSolutionsTable([(1, 0, 0)]))


def kappa_example_plan():
    yield from bps.mv(kappa, (0.5, .1, 0.5))   

    detectors = [
        kappa.h, kappa.k, kappa.l,
        # I0Mon, diode, scint,
        ]

    # add scan metadata
    geom = kappa.calc.__class__.__name__.lstrip("Calc")
    md = dict(
        komega=kappa.komega.position,
        kappa=kappa.kappa.position,
        kphi=kappa.kphi.position,
        tth=kappa.tth.position,
        wavelength=kappa.calc.wavelength,
        energy=kappa.calc.energy * 10,   # FIXME: calc module uses NM_KEV but should be A_KEV instead
        mode=kappa.calc.engine.mode,
        sample=kappa.calc.sample.name,
        hkl_engine=kappa.engine.name,
        diffractometer_geometry=geom,
    )
    yield from bp.scan(detectors, kappa.l, 0.5, 1.5, 11, md=md)