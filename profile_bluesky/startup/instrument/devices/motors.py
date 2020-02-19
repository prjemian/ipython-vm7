
"""
configure the motors
"""

__all__ = """
    m1 m2 m3 m4 
    m5 m6 m7 m8
""".split()

from ophyd import Device, Component, EpicsSignal, EpicsMotor

from apstools.devices import EpicsMotorLimitsMixin
from ..session_logs import logger
logger.info(__file__)


class MyMotor(EpicsMotorLimitsMixin, EpicsMotor):
    "add support for setting/chaning motor limits and resolution"
    steps_per_rev = Component(EpicsSignal, ".SREV", kind="omitted")


m1 = MyMotor('sky:m1', name='m1', labels=("motor",))
m2 = MyMotor('sky:m2', name='m2', labels=("motor",))
m3 = MyMotor('sky:m3', name='m3', labels=("motor",))
m4 = MyMotor('sky:m4', name='m4', labels=("motor",))
m5 = MyMotor('sky:m5', name='m5', labels=("motor",))
m6 = MyMotor('sky:m6', name='m6', labels=("motor",))
m7 = MyMotor('sky:m7', name='m7', labels=("motor",))
m8 = MyMotor('sky:m8', name='m8', labels=("motor",))
# m9-16 are now parts of other devices

for m in (m1, m2, m3, m4, 
          m5, m6, m7, m8):
    m.steps_per_rev.put(8000)
del m
