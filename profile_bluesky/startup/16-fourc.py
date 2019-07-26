logger.info(__file__)

"""Four circle diffractometer (simulated)"""

import gi
gi.require_version('Hkl', '5.0')
from hkl.diffract import E4CV  #this works for mu=0
from ophyd import PseudoSingle

MOTOR_PV_OMEGA = "vm7:m9"
MOTOR_PV_CHI = "vm7:m10"
MOTOR_PV_PHI = "vm7:m11"
MOTOR_PV_TTH = "vm7:m12"


class Fourc(E4CV):
    h = Component(PseudoSingle, '')
    k = Component(PseudoSingle, '')
    l = Component(PseudoSingle, '')

    omega = Component(EpicsMotor, MOTOR_PV_OMEGA)
    chi =   Component(EpicsMotor, MOTOR_PV_CHI)
    phi =   Component(EpicsMotor, MOTOR_PV_PHI)
    tth =   Component(EpicsMotor, MOTOR_PV_TTH)


fourc = Fourc('', name='fourc')
logger.info(f"{fourc.name} modes: {fourc.engine.modes}")
fourc.calc.engine.mode = 'bissector'    # constrain tth = 2 * omega
logger.info(f"selected mode: {fourc.calc.engine.mode}")
