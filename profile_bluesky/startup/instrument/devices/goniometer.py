
"""
hypothetical motorized goniometer head

simulate as stepper motors
"""

__all__ = ['goniometer',]

from instrument.session_logs import logger
logger.info(__file__)

from apstools.devices import EpicsMotorLimitsMixin
from ophyd import Component, Device, EpicsMotor, EpicsSignal
import time

class MyMotor(EpicsMotorLimitsMixin, EpicsMotor):
    "add support for setting/changing motor limits and resolution"
    description = Component(EpicsSignal, ".DESC", kind="omitted")
    steps_per_rev = Component(EpicsSignal, ".SREV", kind="omitted")

    def initial_reconfig(self, egu, srev, lo, hi):
        """
        initial motor record configuration, not a plan

        Don't do this on production IOCs
        since these parameters are usually 
        required by hardware configurations.
        """
        self.description.put(self.name)
        self.motor_egu.put(egu)
        self.steps_per_rev.put(srev)
        self.soft_limit_hi.put(max(lo, hi))
        # short wait to let CA monitors update
        time.sleep(0.001)
        self.soft_limit_lo.put(min(lo, hi))


class MyGoniometer(Device):  
    """
    hypothetical motorized goniometer head
    """    
    # X horizontal translation
    x = Component(MyMotor, 'sky:m9', labels=["motor", "goniometer"])

    # X tilt
    xt = Component(MyMotor, 'sky:m10', labels=["motor", "goniometer"])

    # Z horizontal translation
    z = Component(MyMotor, 'sky:m11', labels=["motor", "goniometer"])

    # Z tilt
    zt = Component(MyMotor, 'sky:m12', labels=["motor", "goniometer"])


goniometer = MyGoniometer(name="goniometer")

# configure our example IOC motors

goniometer.x.initial_reconfig("mm", 8000, -21, 21)
goniometer.xt.initial_reconfig("degrees", 8000, -35, 35)
goniometer.z.initial_reconfig("mm", 8000, -21, 21)
goniometer.zt.initial_reconfig("degrees", 8000, -35, 35)
