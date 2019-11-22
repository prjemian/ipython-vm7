logger.info(__file__)

"""signals"""

# APS only:
# aps = APS_devices.ApsMachineParametersDevice(name="aps")
# sd.baseline.append(aps)

# undulator = APS_devices.ApsUndulatorDual("ID45", name="undulator")
# sd.baseline.append(undulator)


# simulate a shutter (no hardware required)
shutter = SimulatedApsPssShutterWithStatus(name="shutter")
shutter.delay_s = 0.05 # shutter needs short recovery time after moving

calcs = APS_synApps.UserCalcsDevice("sky:", name="calcs")
calcouts = APS_synApps.UserCalcoutDevice("sky:", name="calcouts")

# demo: use this swait record to make a "noisy" detector signal
noisy = EpicsSignalRO('sky:userCalc1', name='noisy', labels=("detectors",))

calcs.enable.put(1)
epics.caput(m1.prefix + ".SREV", 8000)

APS_devices.setup_lorentzian_swait(
    calcs.calc1,
    m1.user_readback,
    center = 2*np.random.random() - 1,
    width = 0.015 * np.random.random(),
    scale = 10000 * (9 + np.random.random()),
    noise=0.05,
)

def example_tune():
    p0 = m1.position
    print(f"starting position: {p0}")
    yield from bp.scan([noisy], m1, -2, 2, 53)
    cen = bec.peaks["cen"].get(noisy.name)
    fwhm = bec.peaks["fwhm"].get(noisy.name)
    print(f"rough tune: cen={cen}, fwhm={fwhm}")

    if cen is None:
        yield from bps.mv(m1, p0)
    else:
        yield from bps.mv(m1, cen)
        yield from bp.rel_scan([noisy], m1, -fwhm, fwhm, 47)
        cen = bec.peaks["cen"][noisy.name]
        fwhm = bec.peaks["fwhm"][noisy.name]
        print(f"fine tune: cen={cen}, fwhm={fwhm}")
        yield from bps.mv(m1, cen)

    print(f"final position: {m1.position}")
