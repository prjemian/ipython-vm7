
"""
configure the motors
"""

import logging
from ophyd import Device, Component, EpicsSignal, EpicsMotor

logger = logging.getLogger(__name__)
logger.info(__file__)

class StepsPerRevMotor(EpicsMotor):
    steps_per_rev = Component(EpicsSignal, ".SREV", kind="omitted")


m1 = StepsPerRevMotor('sky:m1', name='m1', labels=("motor",))
m2 = StepsPerRevMotor('sky:m2', name='m2', labels=("motor",))
m3 = StepsPerRevMotor('sky:m3', name='m3', labels=("motor",))
m4 = StepsPerRevMotor('sky:m4', name='m4', labels=("motor",))
m5 = StepsPerRevMotor('sky:m5', name='m5', labels=("motor",))
m6 = StepsPerRevMotor('sky:m6', name='m6', labels=("motor",))
m7 = StepsPerRevMotor('sky:m7', name='m7', labels=("motor",))
m8 = StepsPerRevMotor('sky:m8', name='m8', labels=("motor",))

m16 = StepsPerRevMotor('sky:m16', name='m16', labels=("motor",))

for m in (m1, m2, m3, m4, m5, m6, m7, m8, m16):
    m.steps_per_rev.put(8000)
del m
