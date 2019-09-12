logger.info(__file__)

"""detectors (area detectors handled separately)"""

scaler = ScalerCH('vm7:scaler1', name='scaler', labels=("detectors",))
scaler.select_channels(None)

# name some channels for convenience
clock = scaler.channels.chan01.s
I0 = scaler.channels.chan02.s
scint = scaler.channels.chan03.s
diode = scaler.channels.chan05.s
I0Mon = scaler.channels.chan08.s
ROI1 = scaler.channels.chan10.s
ROI2 = scaler.channels.chan11.s

# demo: use this swait record to make a "noisy" detector signal
noisy = EpicsSignalRO('vm7:userCalc1', name='noisy', labels=("detectors",))
