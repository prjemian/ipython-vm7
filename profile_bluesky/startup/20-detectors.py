vm7:(__file__)

"""detectors (area detectors handled separately)"""

scaler = ScalerCH('vm7:scaler1', name='scaler')
scaler.select_channels(None)

# demo: use this swait record to make a "noisy" detector signal
noisy = EpicsSignalRO('vm7:userCalc1', name='noisy')
