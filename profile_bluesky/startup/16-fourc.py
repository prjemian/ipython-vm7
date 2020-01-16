logger.info(__file__)

"""Four circle diffractometer (simulated)"""

use_fourc_diffractometer = True

if use_fourc_diffractometer:
    import gi
    gi.require_version('Hkl', '5.0')
    from hkl.diffract import E4CV  #this works for mu=0
    from hkl.util import Lattice
    from ophyd import PseudoSingle

    MOTOR_PV_OMEGA = "sky:m9"
    MOTOR_PV_CHI = "sky:m10"
    MOTOR_PV_PHI = "sky:m11"
    MOTOR_PV_TTH = "sky:m12"

    AxisConstraints = collections.namedtuple(
        "AxisConstraints", 
        "low_limit high_limit value fit".split())

    class FourCircleDiffractometer(E4CV):
        h = Component(PseudoSingle, '', labels=("hkl", "fourc"))
        k = Component(PseudoSingle, '', labels=("hkl", "fourc"))
        l = Component(PseudoSingle, '', labels=("hkl", "fourc"))

        omega = Component(EpicsMotor, MOTOR_PV_OMEGA, labels=("motor", "fourc"))
        chi =   Component(EpicsMotor, MOTOR_PV_CHI, labels=("motor", "fourc"))
        phi =   Component(EpicsMotor, MOTOR_PV_PHI, labels=("motor", "fourc"))
        tth =   Component(EpicsMotor, MOTOR_PV_TTH, labels=("motor", "fourc"))

        # calculate using the current UB matrix & constraints
        def forwardSolutionsTable(self, reflections, full=False):
            """
            make a table of the computed solutions for each of the supplied hkl reflections
            """
            _table = pyRestTable.Table()
            motors = self.real_positioners._fields
            _table.labels = "(hkl) solution".split() + list(motors)
            for reflection in reflections:
                try:
                    solutions = self.calc.forward(reflection)
                except ValueError as exc:
                    solutions = exc
                if isinstance(solutions, ValueError):
                    row = [reflection, "none"]
                    row += ["" for m in motors]
                    _table.addRow(row)
                else:
                    for i, s in enumerate(solutions):
                        row = [reflection, i]
                        row += [f"{getattr(s, m):.5f}" for m in motors]
                        _table.addRow(row)
                        if not full:    # show all solutions?
                            break
            return _table


    fourc = FourCircleDiffractometer('', name='fourc')
    logger.info(f"{fourc.name} modes: {fourc.engine.modes}")
    fourc.calc.engine.mode = 'bissector'    # constrain tth = 2 * omega
    logger.info(f"selected mode: {fourc.calc.engine.mode}")

    # Q: How to reset to default constraints?
    # TODO: remember current constraints (use a stack to push/pop)

    # define some constraints in a dictionary
    diffractometer_constraints = {
        # axis: AxisConstraints(lo_limit, hi_limit, value, fit)
        "omega": AxisConstraints(-150, 150, 0, True),
        "tth": AxisConstraints(-10, 142, 0, True),
        "chi": AxisConstraints(-120, 120, 0, True),
        
        # # we don't have these axes. Fix them to 0
        # "phi": AxisConstraints(0, 0, 0, False),
        # "chi": AxisConstraints(0, 0, 0, False),
        
        # # Attention naming convention inverted at the detector stages!
        # "delta": AxisConstraints(-5, 180, 0, True),
        # "gamma": AxisConstraints(-5, 180, 0, True),
    }

    # apply constraints from our dictionary
    for axis, constraints in diffractometer_constraints.items():
        fourc.calc[axis].limits = (constraints.low_limit, constraints.high_limit)
        fourc.calc[axis].value = constraints.value
        fourc.calc[axis].fit = constraints.fit

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


def fourc_example_plan():
    reflections = (
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
