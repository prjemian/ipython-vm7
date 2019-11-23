logger.info(__file__)

"""local, custom Device definitions"""

class MyRegisters(Device):
    decimal1 = Component(EpicsSignal, "float1")
    decimal2 = Component(EpicsSignal, "float2")
    decimal3 = Component(EpicsSignal, "float3")
    decimal4 = Component(EpicsSignal, "float4")
    decimal5 = Component(EpicsSignal, "float5")

    bit1 = Component(EpicsSignal, "bit1")
    bit2 = Component(EpicsSignal, "bit2")
    bit3 = Component(EpicsSignal, "bit3")
    bit4 = Component(EpicsSignal, "bit4")
    bit5 = Component(EpicsSignal, "bit5")

    whole1 = Component(EpicsSignal, "int1")
    whole2 = Component(EpicsSignal, "int2")
    whole3 = Component(EpicsSignal, "int3")
    whole4 = Component(EpicsSignal, "int4")
    whole5 = Component(EpicsSignal, "int5")

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
