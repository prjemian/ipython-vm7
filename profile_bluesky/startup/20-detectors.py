logger.info(__file__)

"""detectors (area detectors handled separately)"""

scaler = ScalerCH('vm7:scaler1', name='scaler', labels=("detectors",))
scaler.select_channels(None)

# demo: use this swait record to make a "noisy" detector signal
noisy = EpicsSignalRO('vm7:userCalc1', name='noisy', labels=("detectors",))
