logger.info(__file__)

"""detectors (area detectors handled separately)"""

scaler = ScalerCH('sky:scaler1', name='scaler', labels=("detectors",))
scaler.select_channels(None)

# name some channels for convenience
clock = scaler.channels.chan01.s
I0 = scaler.channels.chan02.s
scint = scaler.channels.chan03.s
diode = scaler.channels.chan05.s
I0Mon = scaler.channels.chan08.s
ROI1 = scaler.channels.chan10.s
ROI2 = scaler.channels.chan11.s

for obj in (clock, I0, scint, diode, I0Mon, ROI1, ROI2):
    obj._ophyd_labels_ = set(list(obj._ophyd_labels_) + ["counter"])

# demo: use this swait record to make a "noisy" detector signal
noisy = EpicsSignalRO('sky:userCalc1', name='noisy', labels=("detectors",))
