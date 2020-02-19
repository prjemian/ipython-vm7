
"""
example XY stage with a XZ table
"""

__all__ = ['samplestage',]

from instrument.session_logs import logger
logger.info(__file__)

from apstools.devices import EpicsMotorLimitsMixin
from ophyd import Component, Device, EpicsMotor
import time

class MyMotor(EpicsMotorLimitsMixin, EpicsMotor):
    "adds support for setting/changing motor limits"

class StageTable(Device):  
    """
    table for the sample stage
    """    
    # horizontal translation transverse to incoming beam
    x = Component(MyMotor, 'sky:m13', labels=["motor", "table"])
    # horizontal translation parallel to incoming beam
    z = Component(MyMotor, 'sky:m14', labels=["motor", "table"])

class SampleStage(Device):  
    """
    table for the sample stage
    """    
    # horizontal translation transverse to incoming beam
    x = Component(MyMotor, 'sky:m15', labels=["motor", "sample"])
    # vertical translation transverse to incoming beam
    y = Component(MyMotor, 'sky:m16', labels=["motor", "sample"])
    # support table
    table = Component(StageTable)

samplestage = SampleStage(name="samplestage")
