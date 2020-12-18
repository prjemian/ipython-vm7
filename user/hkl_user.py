"""
Provide a simplified UI for hklpy diffractometer users.

The user must define a diffractometer instance, then
register that instance here calling `selectDiffractometer(instance)`.

FUNCTIONS

.. autosummary::

    ~calcUB
    ~listSamples
    ~newSample
    ~selectDiffractometer
    ~setor
    ~showSample
    ~showSelectedDiffractometer
"""

__all__ = """
    calcUB
    listSamples
    newSample
    selectDiffractometer
    setor
    showSample
    showSelectedDiffractometer

EXAMPLES::

    In [1]: %run -m hkl_user
    I Thu-23:02:52 - /home/mintadmin/.ipython/user/hkl_user.py

    In [2]: selectDiffractometer(fourc)

    In [3]: showSelectedDiffractometer()
    fourc

    In [4]: newSample("silicon", 5.431, 5.431, 5.431, 90, 90, 90)
    HklSample(name='silicon', lattice=LatticeTuple(a=5.431, b=5.431, c=5.431, alpha=90.0, beta=90.0, gamma=90.0), ux=Parameter(name='None (internally: ux)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uy=Parameter(name='None (internally: uy)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uz=Parameter(name='None (internally: uz)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), U=array([[1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]]), UB=array([[ 1.15691131e+00, -7.08403864e-17, -7.08403864e-17],
        [ 0.00000000e+00,  1.15691131e+00, -7.08403864e-17],
        [ 0.00000000e+00,  0.00000000e+00,  1.15691131e+00]]), reflections=[], reflection_measured_angles=array([], shape=(0, 0), dtype=float64), reflection_theoretical_angles=array([], shape=(0, 0), dtype=float64))

    In [5]: showSample()
    HklSample(name='silicon', lattice=LatticeTuple(a=5.431, b=5.431, c=5.431, alpha=90.0, beta=90.0, gamma=90.0), ux=Parameter(name='None (internally: ux)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uy=Parameter(name='None (internally: uy)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uz=Parameter(name='None (internally: uz)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), U=array([[1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]]), UB=array([[ 1.15691131e+00, -7.08403864e-17, -7.08403864e-17],
        [ 0.00000000e+00,  1.15691131e+00, -7.08403864e-17],
        [ 0.00000000e+00,  0.00000000e+00,  1.15691131e+00]]), reflections=[], reflection_measured_angles=array([], shape=(0, 0), dtype=float64), reflection_theoretical_angles=array([], shape=(0, 0), dtype=float64))

    In [6]: listSamples()
    HklSample(name='main', lattice=LatticeTuple(a=1.54, b=1.54, c=1.54, alpha=90.0, beta=90.0, gamma=90.0), ux=Parameter(name='None (internally: ux)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uy=Parameter(name='None (internally: uy)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uz=Parameter(name='None (internally: uz)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), U=array([[1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]]), UB=array([[ 4.07999046e+00, -2.49827363e-16, -2.49827363e-16],
        [ 0.00000000e+00,  4.07999046e+00, -2.49827363e-16],
        [ 0.00000000e+00,  0.00000000e+00,  4.07999046e+00]]), reflections=[], reflection_measured_angles=array([], shape=(0, 0), dtype=float64), reflection_theoretical_angles=array([], shape=(0, 0), dtype=float64))
    HklSample(name='silicon', lattice=LatticeTuple(a=5.431, b=5.431, c=5.431, alpha=90.0, beta=90.0, gamma=90.0), ux=Parameter(name='None (internally: ux)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uy=Parameter(name='None (internally: uy)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), uz=Parameter(name='None (internally: uz)', limits=(min=-180.0, max=180.0), value=0.0, fit=True, inverted=False, units='Degree'), U=array([[1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]]), UB=array([[ 1.15691131e+00, -7.08403864e-17, -7.08403864e-17],
        [ 0.00000000e+00,  1.15691131e+00, -7.08403864e-17],
        [ 0.00000000e+00,  0.00000000e+00,  1.15691131e+00]]), reflections=[], reflection_measured_angles=array([], shape=(0, 0), dtype=float64), reflection_theoretical_angles=array([], shape=(0, 0), dtype=float64))

    In [7]: %mov fourc.omega -145.451 fourc.chi 90 fourc.phi 0 fourc.tth 69.0966

    In [8]: r2 = setor(0, 4, 0)


""".split()

from instrument.session_logs import logger

logger.info(__file__)

import gi
gi.require_version("Hkl", "5.0")
from hkl.diffract import Diffractometer
from hkl.util import Lattice


_geom_ = None  # selected diffractometer geometry


def _check_selected_(*args, **kwargs):
    """Raise ValueError i no diffractometer is selected."""
    if _geom_ is None:
        raise ValueError(
            "No diffractometer selected."
            " Call 'selectDiffractometer(diffr)' where"
            " 'diffr' is a diffractometer instance."
        )


def calcUB(r1, r2, wavelength=None):
    """Compute the UB matrix with two reflections for a given energy."""
    _check_selected_()
    if wavelength is not None:
        _geom_.calc.wavelength = wavelength
    _geom_.calc.sample.compute_UB(r1, r2)
    print(_geom_.calc.sample.UB)


def listSamples():
    """List all defined crystal samples."""
    _check_selected_()
    for sample in _geom_.calc._samples.values():
        # TODO: show which one is the current default sample
        print(sample)


def newSample(nm, a, b, c, alpha, beta, gamma):
    """Define a new crystal sample."""
    _check_selected_()
    if nm in _geom_.calc._samples:
        logger.warning("Sample '%s' is already defined.", nm)
    else:
        lattice=Lattice(
                a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)
        _geom_.calc.new_sample(nm, lattice=lattice)
    showSample()


def selectDiffractometer(instrument=None):
    """Name the diffractometer to be used."""
    global _geom_
    if instrument is None or isinstance(instrument, Diffractometer):
        _geom_ = instrument
    else:
        raise TypeError(
            f"{instrument} must be a 'Diffractometer' subclass"
        )


def setor(h, k, l, **kwargs):
    """Define a crystal reflection and its motor positions."""
    _check_selected_()
    if len(kwargs) == 0:
        pos = _geom_.real_position
    else:
        pos = _geom_.calc.Position(**kwargs)
    refl = _geom_.calc.sample.add_reflection(h, k, l, position=pos)
    return refl


def showSample():
    """Print the default sample name and crystal lattice."""
    _check_selected_()
    print(_geom_.calc.sample)


def showSelectedDiffractometer(instrument=None):
    """Print the name of the selected diffractometer."""
    if _geom_ is None:
        print("No diffractometer selected.")
    print(_geom_.name)
