
"""
six circle diffractometer (simulated)

```
Created at 2016-06-02 14:12

Crystal    EuPtIn4_eh1_ver

Wavelength 1.62751693358

A 4.542 B 16.955 C 7.389
Alpha 90.0 Beta 90.0 Gamma 90.0

R0 0 0.0 8.0 0.0 0 1 0.0 22.31594 89.1377 0.0 0.0 45.15857
R1 1 0.0 12.0 1.0 0 1 0.0 34.96232 78.3139 0.0 0.0 71.8007

Engine hkl

Mode constant_phi_vertical

PsiRef not available in current engine mode

AutoEnergyUpdate 1

U00 1.381 U01 -0.002 U02 -0.054 
U10 0.005 U11 0.371 U12 -0.013 
U20 0.087 U21 0.006 U22 0.849 

Ux 0.878929693221 Uy -3.6132870009 Uz 0.263869539307
```
"""

__all__ = [
    "sixc",
    "sixc_example",
    "sixc_example_constraints",
    "sixc_example_plan",
]

from ..session_logs import logger
logger.info(__file__)

import gi
gi.require_version('Hkl', '5.0')
# FIXME: Aaaaaack!  Next line dumps core! On fresh Ubuntu 19.10
from hkl.diffract import E6C  #this works for mu=0
# Segmentation fault (core dumped)
from hkl.util import Lattice

from bluesky import plans as bp
from bluesky import plan_stubs as bps

from ophyd import Component
from ophyd import PseudoSingle
from ophyd import SoftPositioner

from apstools.diffractometer import Constraints, DiffractometerMixin
# from .scaler import I0Mon, diode, scint


class SixCircleDiffractometer(DiffractometerMixin, E6C):
    h = Component(PseudoSingle, '', labels=("hkl", "sixc"))
    k = Component(PseudoSingle, '', labels=("hkl", "sixc"))
    l = Component(PseudoSingle, '', labels=("hkl", "sixc"))

    mu    = Component(SoftPositioner, labels=("motor", "sixc"))
    omega = Component(SoftPositioner, labels=("motor", "sixc"))
    chi   = Component(SoftPositioner, labels=("motor", "sixc"))
    phi   = Component(SoftPositioner, labels=("motor", "sixc"))
    gamma = Component(SoftPositioner, labels=("motor", "sixc"))
    delta = Component(SoftPositioner, labels=("motor", "sixc"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # since this diffractometer uses simulated motors,
        # prime the SoftPositioners (motors) with initial values
        # otherwise, position == None --> describe, etc gets borked
        for axis in (self.mu, self.omega, 
                     self.chi, self.phi, 
                     self.gamma, self.delta):
            axis.move(0)


sixc = SixCircleDiffractometer('', name='sixc', , labels=("diffractometer", "sixc"))


def sixc_example():
    """
    Example from *hkl*: `hkl/tests/bindings/crystal.ini`
    """
    sixc.calc.engine.mode = "constant_phi_vertical"

    sixc.calc.new_sample('EuPtIn4_eh1_ver', 
        lattice=Lattice(
            a=4.542, b=16.955, c=7.389, 
            alpha=90.0, beta=90.0, gamma=90.0))
    
    sixc.calc.wavelength = 1.62751693358 # use angstrom
    
    r1 = sixc.calc.sample.add_reflection(
        0, 8, 0,
        position=sixc.calc.Position(
            mu=0, omega=22.31594, chi=89.1377, phi=0, gamma=0, delta=45.15857))
    r2 = sixc.calc.sample.add_reflection(
        0, 12, 1,
        position=sixc.calc.Position(
            mu=0, omega=34.96232, chi=78.3139, 
            phi=0, gamma=0, delta=71.8007)
            )

    sixc.calc.sample.compute_UB(r1, r2)


def sixc_example_constraints():
    # define some constraints in a dictionary
    diffractometer_constraints = {
        # axis: AxisConstraints(lo_limit, hi_limit, value, fit)
        "mu": AxisConstraints(0, 0, 0, False),
        "omega": AxisConstraints(0, 150, 0, True),
        # "chi": AxisConstraints(-120, 120, 0, True),
        "phi": AxisConstraints(0, 0, 0, False),
        "gamma": AxisConstraints(0, 0, 0, False),
        # "delta": AxisConstraints(-180, 180, 0, True),
    }

    sixc.applyConstraints(diffractometer_constraints)
    sixc.showConstraints()

    # demo calculation, based on HKL_SOURCE/tests/bindings/polarisation.py
    reflections = (
        (0.5, 14.5, 0.43), 
        (0, 8, 0), 
        (0, 12, 1),
    )
    logger.info(sixc.forwardSolutionsTable(reflections, full=True))
    # (0.5, 14.5, 0.43): [0, 51.48568, 84.79259, 0, 0, 89.37964]  # mu, omega, chi, phi, gamma, delta


def sixc_example_plan():
    yield from bps.mv(sixc, (0.5, 14, 0.5))   

    detectors = [
        sixc.h, sixc.k, sixc.l,
        # I0Mon, diode, scint,
        ]

    # add scan metadata
    geom = sixc.calc.__class__.__name__.lstrip("Calc")
    md = dict(
        mu=sixc.mu.position,
        omega=sixc.omega.position,
        chi=sixc.chi.position,
        phi=sixc.phi.position,
        gamma=sixc.gamma.position,
        delta=sixc.delta.position,
        wavelength=sixc.calc.wavelength,
        energy=sixc.calc.energy * 10,   # FIXME: calc module uses NM_KEV but should be A_KEV instead
        mode=sixc.calc.engine.mode,
        sample=sixc.calc.sample.name,
        hkl_engine=sixc.engine.name,
        diffractometer_geometry=geom,
    )
    yield from bp.scan(detectors, sixc.l, 0.5, 1.5, 11, md=md)
