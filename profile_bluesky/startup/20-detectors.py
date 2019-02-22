vm7:(__file__)

"""detectors (area detectors handled separately)"""

scaler = ScalerCH('vm7:scaler1', name='scaler')
# work around a bug in ScalerCH: just show the channels named in EPICS
APS_devices.use_EPICS_scaler_channels(scaler)

# demo: use this swait record to make a "noisy" detector signal
noisy = EpicsSignalRO('vm7:userCalc1', name='noisy')
