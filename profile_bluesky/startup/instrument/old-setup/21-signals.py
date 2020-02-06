logger.info(__file__)

"""signals"""

# from instrument.devices.my_registers import *
from instrument.startup import *
print("loaded instrument.startup")

# APS only:
# aps = APS_devices.ApsMachineParametersDevice(name="aps")
# sd.baseline.append(aps)

# undulator = APS_devices.ApsUndulatorDual("ID45", name="undulator")
# sd.baseline.append(undulator)


# simulate a shutter (no hardware required)
shutter = SimulatedApsPssShutterWithStatus(name="shutter")
shutter.delay_s = 0.05 # shutter needs short recovery time after moving


# demo: use swait records to make "noisy" detector signals
noisy = EpicsSignalRO('sky:userCalc1', name='noisy', labels=("detectors",))

APS_devices.setup_lorentzian_swait(
    calcs.calc1,
    m1.user_readback,
    center = 2*np.random.random() - 1,
    width = 0.015 * np.random.random(),
    scale = 10000 * (9 + np.random.random()),
    noise=0.05,
)

try:
    APS_devices.setup_lorentzian_swait(
        calcs.calc2,
        mover2,
        center = 2*np.random.random() - 1,
        width = 0.015 * np.random.random(),
        scale = 10000 * (9 + np.random.random()),
        noise=0.05,
    )
    calcs.calc2.output_link_pv.put(registers.decimal1.pvname)
except NameError:
    logger.info("variable `registers` is not defined")


print(f"end of {__file__}")
