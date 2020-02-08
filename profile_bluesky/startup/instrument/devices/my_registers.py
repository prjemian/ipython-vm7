
"""
interface EPICS database of general purpose variables
"""

from ophyd import Component, Device, EpicsSignal
from ..session_logs import logger
logger.info(__file__)


class MyRegisters(Device):
    decimal1 = Component(EpicsSignal, "float1", kind="hinted")
    decimal2 = Component(EpicsSignal, "float2", kind="hinted")
    decimal3 = Component(EpicsSignal, "float3", kind="hinted")
    decimal4 = Component(EpicsSignal, "float4", kind="hinted")
    decimal5 = Component(EpicsSignal, "float5", kind="hinted")

    bit1 = Component(EpicsSignal, "bit1")
    bit2 = Component(EpicsSignal, "bit2")
    bit3 = Component(EpicsSignal, "bit3")
    bit4 = Component(EpicsSignal, "bit4")
    bit5 = Component(EpicsSignal, "bit5")

    whole1 = Component(EpicsSignal, "int1", kind="hinted")
    whole2 = Component(EpicsSignal, "int2", kind="hinted")
    whole3 = Component(EpicsSignal, "int3", kind="hinted")
    whole4 = Component(EpicsSignal, "int4", kind="hinted")
    whole5 = Component(EpicsSignal, "int5", kind="hinted")

    text1 = Component(EpicsSignal, "text1", string=True)
    text2 = Component(EpicsSignal, "text2", string=True)
    text3 = Component(EpicsSignal, "text3", string=True)
    text4 = Component(EpicsSignal, "text4", string=True)
    text5 = Component(EpicsSignal, "text5", string=True)

    textwave1 = Component(EpicsSignal, "textwave1", string=True)
    textwave2 = Component(EpicsSignal, "textwave2", string=True)
    textwave3 = Component(EpicsSignal, "textwave3", string=True)
    textwave4 = Component(EpicsSignal, "textwave4", string=True)
    textwave5 = Component(EpicsSignal, "textwave5", string=True)


try:
    registers = MyRegisters("IOC:", name="registers")
    det2 = registers.decimal1
    mover2 = registers.decimal2
except Exception:
    print("registers.db IOC is not available")
    registers = None
    det2 = None
    mover2 = None
