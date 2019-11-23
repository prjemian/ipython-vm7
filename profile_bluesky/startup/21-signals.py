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

# demo: use swait records to make "noisy" detector signals
noisy = EpicsSignalRO('sky:userCalc1', name='noisy', labels=("detectors",))

calcs.enable.put(1)

APS_devices.setup_lorentzian_swait(
    calcs.calc1,
    m1.user_readback,
    center = 2*np.random.random() - 1,
    width = 0.015 * np.random.random(),
    scale = 10000 * (9 + np.random.random()),
    noise=0.05,
)


try:
    registers = MyRegisters("IOC:", name="registers")
    det2 = registers.decimal1
    mover2 = registers.decimal2
    APS_devices.setup_lorentzian_swait(
        calcs.calc2,
        mover2,
        center = 2*np.random.random() - 1,
        width = 0.015 * np.random.random(),
        scale = 10000 * (9 + np.random.random()),
        noise=0.05,
    )
    calcs.calc2.output_link_pv.put(registers.decimal1.pvname)
except Exception:
    print("registers.db IOC is not available")
    registers = None
    det2 = None
    mover2 = None
