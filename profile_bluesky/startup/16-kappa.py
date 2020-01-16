logger.info(__file__)

"""Four circle diffractometer (simulated)"""

use_kappa_diffractometer = False

if use_kappa_diffractometer:
    import gi
    gi.require_version('Hkl', '5.0')
    from hkl.diffract import K4CV
    from hkl.util import Lattice
    from ophyd import PseudoSingle

    MOTOR_PV_KOMEGA = "sky:m9"
    MOTOR_PV_KAPPA = "sky:m10"
    MOTOR_PV_KPHI = "sky:m11"
    MOTOR_PV_TTH = "sky:m12"

    AxisConstraints = collections.namedtuple(
        "AxisConstraints", 
        "low_limit high_limit value fit".split())

    # for more configuration ideas, see
    # https://github.com/prjemian/ipython_poof/blob/23db4dd2b00b780a9f021953f4bbf43bfdb78aa6/profile_bluesky/startup/16-tardis.py

    class KappaDiffractometer(K4CV):
        h = Component(PseudoSingle, '', labels=("hkl", "kappa"))
        k = Component(PseudoSingle, '', labels=("hkl", "kappa"))
        l = Component(PseudoSingle, '', labels=("hkl", "kappa"))

        # energy : Signal unless we override it here
        komega = Component(EpicsMotor, MOTOR_PV_KOMEGA, labels=("motor", "kappa"))
        kappa =   Component(EpicsMotor, MOTOR_PV_KOMEGA, labels=("motor", "kappa"))
        kphi =   Component(EpicsMotor, MOTOR_PV_KPHI, labels=("motor", "kappa"))
        tth =   Component(EpicsMotor, MOTOR_PV_TTH, labels=("motor", "kappa"))

        # omega =   Component(SoftPositioner)

    kappa = KappaDiffractometer('', name='kappa')
    logger.info(f"{kappa.name} modes: {kappa.engine.modes}")
    kappa.calc.engine.mode = kappa.engine.modes[0]
    logger.info(f"selected mode: {kappa.calc.engine.mode}")

    # define some constraints in a dictionary
    diffractometer_constraints = {
        # axis: AxisConstraints(lo_limit, hi_limit, value, fit)
        "kappa": AxisConstraints(-10, 87, 0, True),
        "tth": AxisConstraints(-91, 91, 0, True),
        
        # we don't have these axes. Fix them to 0
        "phi": AxisConstraints(0, 0, 0, False),
        "chi": AxisConstraints(0, 0, 0, False),
        "omega": AxisConstraints(0, 0, 0, False),    #kappa.omega.position.real
        
        # # Attention naming convention inverted at the detector stages!
        # "delta": AxisConstraints(-5, 180, 0, True),
        # "gamma": AxisConstraints(-5, 180, 0, True),
    }

    # FIXME: TypeError: argument of type 'NoneType' is not iterable
    # when setting the first limits constraint
    # # apply constraints from our dictionary
    # for axis, constraints in diffractometer_constraints.items():
    #     kappa.calc[axis].limits = (constraints.low_limit, constraints.high_limit)
    #     kappa.calc[axis].value = constraints.value
    #     kappa.calc[axis].fit = constraints.fit


    # define a crystal by its lattice
    kappa.calc.new_sample('cubic_sample', 
            lattice=Lattice(
                a=5.14, b=5.14, c=5.14, 
                alpha=90, beta=90, gamma=90))

    # calculate using the default UB matrix

    print(kappa.calc.forward((1, 0, 0)))
