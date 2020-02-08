

"""Four circle diffractometer (simulated)"""

import logging
logger = logging.getLogger(__name__)
logger.info(__file__)

import gi
gi.require_version('Hkl', '5.0')
from hkl.diffract import E4CV, E4CH  #this works for mu=0
from hkl.util import Lattice

from bluesky import plans as bp
from bluesky import plan_stubs as bps

from ophyd import Component
from ophyd import EpicsMotor
from ophyd import PseudoSingle
from ophyd import SoftPositioner

from .diffractometer import AxisConstraints
from .diffractometer import DiffractometerMixin
from .scaler import I0Mon, diode, scint


use_fourc_diffractometer = True

if use_fourc_diffractometer:

    MOTOR_PV_OMEGA = "sky:m9"
    MOTOR_PV_CHI = "sky:m10"
    MOTOR_PV_PHI = "sky:m11"
    MOTOR_PV_TTH = "sky:m12"


    class FourCircleDiffractometer(DiffractometerMixin, E4CV):
        h = Component(PseudoSingle, '', labels=("hkl", "fourc"))
        k = Component(PseudoSingle, '', labels=("hkl", "fourc"))
        l = Component(PseudoSingle, '', labels=("hkl", "fourc"))

        omega = Component(EpicsMotor, MOTOR_PV_OMEGA, labels=("motor", "fourc"))
        chi =   Component(EpicsMotor, MOTOR_PV_CHI, labels=("motor", "fourc"))
        phi =   Component(EpicsMotor, MOTOR_PV_PHI, labels=("motor", "fourc"))
        tth =   Component(EpicsMotor, MOTOR_PV_TTH, labels=("motor", "fourc"))

    fourc = FourCircleDiffractometer('', name='fourc')
    logger.info(f"{fourc.name} modes: {fourc.engine.modes}")
    fourc.calc.engine.mode = fourc.engine.modes[0]  # 'bissector' - constrain tth = 2 * omega
    logger.info(f"selected mode: {fourc.calc.engine.mode}")

    # reflections = [(h-2,k-2,l-2) for h in range(5) for k in range(5) for l in range(5)]
    reflections = (
        (1,0,0), 
        (1,1,0), 
        (1,0,1), 
        (1,1,1),
    )

    print(fourc.forwardSolutionsTable(reflections, full=True))


def fourc_example():
    """
    epitaxial thin film of Mn3O4 on MgO substrate
    
    see: http://www.rigaku.com/downloads/journal/Vol16.1.1999/cguide.pdf
    """

    fourc.calc.new_sample('Mn3O4/MgO thin film', 
        lattice=Lattice(
            a=5.72, b=5.72, c=9.5, 
            alpha=90.0, beta=90.0, gamma=90.0))
    
    fourc.calc.wavelength = 12.3984244 / 8.04   # Cu Kalpha
    
    r1 = fourc.calc.sample.add_reflection(
        -1.998, -1.994, 4.011,
        position=fourc.calc.Position(
            tth=80.8769, omega=40.6148, chi=0.647, phi=-121.717))
    r2 = fourc.calc.sample.add_reflection(
        -0.997, -0.997, 2.009,
        position=fourc.calc.Position(
            tth=28.695, omega=14.4651, chi=-48.8860, phi=-88.758))
    fourc.calc.sample.compute_UB(r1, r2)


def example_fourc_constraints():
    # define some constraints in a dictionary
    diffractometer_constraints = {
        # axis: AxisConstraints(lo_limit, hi_limit, value, fit)
        # "omega": AxisConstraints(-150, 150, 0, True),
        # "tth": AxisConstraints(-10, 142, 0, True),
        # "chi": AxisConstraints(-120, 120, 0, True),
        
        # # we don't have these axes. Fix them to 0
        # "phi": AxisConstraints(0, 0, 0, False),
        # "chi": AxisConstraints(0, 0, 0, False),
        
        # # Attention naming convention inverted at the detector stages!
        # "delta": AxisConstraints(-5, 180, 0, True),
        # "gamma": AxisConstraints(-5, 180, 0, True),
    }

    fourc.applyConstraints(diffractometer_constraints)

def fourc_example_plan():
    reflections = (
        (-2,-2,4), 
        (-1,-1,2), 
        (-2,1,1), 
        (-3,0,5), 
        (0,3,1), 
        (0,3,.5), 
        (0,3,1.5),
    )
    print(fourc.forwardSolutionsTable(reflections))
    yield from bps.mv(fourc, (0, 3, 1))   

    detectors = [
        fourc.h, fourc.k, fourc.l,
        # fourc.omega, fourc.chi, fourc.phi, fourc.tth,
        I0Mon, diode, scint,
        ]
    yield from bp.scan(detectors, fourc.l, 0.5, 1.5, 11)


def fourc_example_LNO_LAO():
    """
    example from APS 33BM

    sample: LNO_LAO
    crystal:  3.781726143 3.791444574 3.79890313 90.2546203 90.01815424 89.89967858
    geometry: fourc
    mode: 0 (Omega equals zero)
    lambda: 1.239424258
    motors: 2-theta     omega       chi       phi
    r1: (0, 0, 2) 38.09875 19.1335 90.0135 0
    r2: (1, 1, 3) 65.644 32.82125 115.23625 48.1315
    Q: (2, 2, 1.9) 67.78225 33.891 145.985 48.22875
    UB: -1.658712442 0.09820024135 -0.000389705578
        -0.09554990312 -1.654278629 0.00242844486
        0.0002629818914 0.009815746824 1.653961812
    
    another example for sixc
        sample: JL124_1
        crystal:  3.905 3.905 3.905 90 90 90
        geometry: sixc
        mode: 12 (Z-Axis with Azimuth fixed and Chi, Phi set to -Sigma, -Tau)
        lambda: 0.8265616267
        motors: Delta     Theta       Chi       Phi        Mu     Gamma
        r1: (0, 0, 2) 0.003 90 0.5799999712 239.9999477 12.102 12.9945
        r2: (3, 0, 3) 47.18 90 0.5799999712 239.9999477 21.77425 15.7375
        Q: (2.99804, 0.00216068, 2.99661) 47.14125 90.089 0.58 239.94275 21.73025 15.7375
        UB: 1.207702707 1.248454819 0.002095582696 
            -1.485612421 0.9118074731 0.003241829804 
            -0.0173752388 0.02282507942 1.651530555
    """


class Fourc_LNO_LAO_Diffractometer(DiffractometerMixin, E4CH):
    # sample: LNO_LAO
    # crystal:  3.781726143 3.791444574 3.79890313 90.2546203 90.01815424 89.89967858
    # geometry: fourc
    # mode: 0 (Omega equals zero)
    # lambda: 1.239424258
    # r1: (0, 0, 2) 38.09875 19.1335 90.0135 0
    # r2: (1, 1, 3) 65.644 32.82125 115.23625 48.1315
    #
    # Q: (2, 2, 1.9) 67.78225 33.891 145.985 48.22875
    # UB: -1.658712442 0.09820024135 -0.000389705578
    #     -0.09554990312 -1.654278629 0.00242844486
    #     0.0002629818914 0.009815746824 1.653961812

    h = Component(PseudoSingle, '', labels=("hkl", "lnolao"))
    k = Component(PseudoSingle, '', labels=("hkl", "lnolao"))
    l = Component(PseudoSingle, '', labels=("hkl", "lnolao"))

    omega = Component(SoftPositioner, labels=("motor", "lnolao"))
    chi =   Component(SoftPositioner, labels=("motor", "lnolao"))
    phi =   Component(SoftPositioner, labels=("motor", "lnolao"))
    tth =   Component(SoftPositioner, labels=("motor", "lnolao"))


lnolao = Fourc_LNO_LAO_Diffractometer('', name='lnolao')
lnolao.calc.engine.mode = "constant_omega"
logger.info(f"selected mode: {lnolao.calc.engine.mode}")
lnolao.applyConstraints({
    "tth": AxisConstraints(-180, 180, 0, True),
    "omega": AxisConstraints(0, 0, 0, False),
    "chi": AxisConstraints(-180, 180, 0, True),
    "phi": AxisConstraints(-180, 180, 0, True),
    })

# give initial values to all positioners
for m in lnolao.real_positioners._fields:
    getattr(lnolao, m).move(0)

lnolao.calc.new_sample('LNO_LAO 33BM', 
    lattice=Lattice(
        a=3.781726143, b=3.791444574, c=3.79890313, 
        alpha=90.2546203, beta=90.01815424, gamma=89.89967858))

lnolao.calc.wavelength = 1.239424258 / 10   # given angstrom, uses nm
lnolao.calc.energy = 10

r1 = lnolao.calc.sample.add_reflection(
    0, 0, 2,
    position=lnolao.calc.Position(
        tth=38.09875, omega=19.1335, chi=90.0135, phi=0))
r2 = lnolao.calc.sample.add_reflection(
    1, 1, 3,
    position=lnolao.calc.Position(
        tth=65.644, omega=32.82125, chi=145.985, phi=48.22875))
lnolao.calc.sample.compute_UB(r1, r2)
print(lnolao.UB.value)
"""
[[-9.55734534e-02 -1.65427724e+00  2.42844485e-03]
 [-1.65871109e+00  9.82237292e-02 -3.89705577e-04]
 [-2.63016876e-04 -9.81484255e-03 -1.65396181e+00]]
"""

print(
    lnolao.forwardSolutionsTable(
        [(2, 2, 1.9),
        (0, 0, 2),
        (1, 1, 3),], 
        full=True))
"""
=========== ======== ======= ========= ======== ========
(hkl)       solution omega   chi       phi      tth     
=========== ======== ======= ========= ======== ========
(2, 2, 1.9) 0        0.00000 -34.07529 44.37100 -6.39529
(2, 2, 1.9) 1        0.00000 145.92471 44.37100 6.39529 
(0, 0, 2)   none                                        
(1, 1, 3)   0        0.00000 -64.97701 40.81909 -6.21577
(1, 1, 3)   1        0.00000 115.02299 40.81909 6.21577 
=========== ======== ======= ========= ======== ========
"""
