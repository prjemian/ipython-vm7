
"""
Huber1003 motorized goniometer head

simulate as stepper motors
"""

__all__ = ['h1003',]

from instrument.session_logs import logger
logger.info(__file__)

from apstools.devices import EpicsMotorLimitsMixin
from ophyd import Component, Device, EpicsMotor, EpicsSignal
import time

class MyMotor(EpicsMotorLimitsMixin, EpicsMotor):
    "add support for setting/changing motor limits and resolution"
    steps_per_rev = Component(EpicsSignal, ".SREV", kind="omitted")

class Huber1003Goniometer(Device):  
    """
    Huber1003 motorized goniometer head
    """    
    # X translation
    x = Component(MyMotor, 'sky:m9', labels=["motor", "h1003"])

    # X tilt
    xt = Component(MyMotor, 'sky:m10', labels=["motor", "h1003"])

    # Z translation
    z = Component(MyMotor, 'sky:m11', labels=["motor", "h1003"])

    # Z tilt
    zt = Component(MyMotor, 'sky:m12', labels=["motor", "h1003"])


h1003 = Huber1003Goniometer(name="h1003")

# configure our example IOC motors
#  Don't do this on production IOCs
#  since these are usually hardware configurations

# configure for higher resolution
for m in (h1003.x, h1003.xt, h1003.z, h1003.zt):
    m.steps_per_rev.put(8000)

# look like translations
h1003.x.motor_egu.put("mm")
h1003.z.motor_egu.put("mm")

# look like tilts (rotations)
h1003.xt.motor_egu.put("degrees")
h1003.zt.motor_egu.put("degrees")

# limits of the goniometer motions
h1003.x.soft_limit_hi.put(21)
h1003.xt.soft_limit_hi.put(35)
h1003.z.soft_limit_hi.put(21)
h1003.zt.soft_limit_hi.put(35)

# short wait to let CA monitors update
time.sleep(0.002)

h1003.x.soft_limit_lo.put(-21)
h1003.xt.soft_limit_lo.put(-35)
h1003.z.soft_limit_lo.put(-21)
h1003.zt.soft_limit_lo.put(-35)
