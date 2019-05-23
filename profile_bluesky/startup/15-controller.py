
print(__file__)

"""mockup of Linkam temperature controller support"""


class Calcout(Device):
    desc = Component(EpicsSignal, ".DESC", string=True)
    calc = Component(EpicsSignal, ".CALC", string=True)
    proc = Component(EpicsSignal, ".PROC")
    scan = Component(EpicsSignal, ".SCAN")
    val = Component(EpicsSignalRO, ".VAL")
    a = Component(EpicsSignal, ".A")
    b = Component(EpicsSignal, ".B")
    c = Component(EpicsSignal, ".C")
    d = Component(EpicsSignal, ".D")
    inpa = Component(EpicsSignal, ".INPA", string=True)
    inpb = Component(EpicsSignal, ".INPB", string=True)
    inpc = Component(EpicsSignal, ".INPC", string=True)
    inpd = Component(EpicsSignal, ".INPD", string=True)


class Controller(Device):
    """common parts of temperature controller support"""
    
    temperature = Component(EpicsSignalRO, ".VAL")
    set_limit = Component(EpicsSignal, ".C", kind="omitted")
    smoothing_factor = Component(EpicsSignal, ".B", kind="omitted")
    pretty_close = Component(EpicsSignal, ".D", kind="omitted")
    
    close_enough  = 1       # requirement: |T - target| must be <= this, degree C
    report_interval  = 5    # time between reports during loop, s
    poll_s = 0.02           # time to wait during polling loop, s
    
    wait_time = Component(Signal, kind="omitted", value=0)
    
    def settled(self, target, close_enough=None):
        """Is temperature close enough to target?"""
        close_enough = self.pretty_close.value
        return abs(self.temperature.get() - target) <= close_enough

    def record_temperature(self):
        """write temperatures as comment"""
        msg = f"Controller Temperature: {self.temperature.value:.3f} C"
        spec_comment(msg)
        print(msg)

    def set_temperature(self, set_point, wait=True, timeout=None):
        """change controller to new temperature set point"""
        yield from bps.mv(self.set_limit, set_point)
        yield from bps.sleep(0.1)   # delay for slow IOC

        msg = f"Controller Set Temperature changed to {set_point} C"
        print(msg)
        spec_comment(msg)
        print(f"wait = {wait}")
        
        if wait:

            _st = DeviceStatus(self.temperature, timeout=timeout)
            started = False

            def changing_cb(value, timestamp, **kwargs):
                if started and self.settled(set_point):
                    _st._finished()

            token = self.temperature.subscribe(changing_cb)
            started = True
            
            t0 = time.time()
            report = time.time()
            # see: https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python
            while not _st.done:
                if time.time() >= report:
                    report += self.report_interval
                    elapsed = time.time() - t0
                    msg = f"Waiting {elapsed:.1f}s"
                    msg += f" to reach {set_point:.2f}C"
                    msg += f", now {self.temperature.get():.2f}C"
                    print(msg)
                yield from bps.sleep(0.02)
            self.record_temperature()
            elapsed = time.time() - t0
            print(f"Total time: {elapsed:.3f}s, settled:{_st.success}")
            self.temperature.unsubscribe(token)


if False:
    # config a calcout record as a pseudo controller
    calcout = Calcout("vm7:userCalcOut9", name="calcout")
    calcout.desc.put("userCalcOut9")
    calcout.calc.put("A*B+(1-B)*C")
    calcout.inpa.put("vm7:userCalcOut9.VAL")
    calcout.b.put(0.5)
    calcout.c.put(0)
    calcout.d.put(0.05)
    calcout.scan.put("1 second")

    for i in range(10, 0, -1):
        print(i)
        time.sleep(1)

    controller = Controller("vm7:userCalcOut9", name="controller")
    controller.record_temperature()
    controller.settled(0)
    RE(controller.set_temperature(25, timeout=10))
    RE(controller.set_temperature(0, timeout=4))
