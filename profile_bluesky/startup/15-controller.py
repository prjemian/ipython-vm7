logger.info(__file__)

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
    tolerance = Component(EpicsSignal, ".D", kind="omitted")
    
    report_interval  = 5    # time between reports during loop, s
    poll_s = 0.02           # time to wait during polling loop, s
    
    wait_time = Component(Signal, kind="omitted", value=0)
    
    def settled(self):
        """Is temperature close enough to target?"""
        diff = abs(self.temperature.get() - self.set_limit.value)
        return diff <= self.tolerance.value

    def record_temperature(self):
        """write temperatures as comment"""
        msg = f"Controller Temperature: {self.temperature.value:.2f} C"
        spec_comment(msg)
        print(msg)

    def set_temperature(self, set_point, wait=True, timeout=None, timeout_fail=False):
        """change controller to new temperature set point"""
        yield from bps.mv(self.set_limit, set_point)
        yield from bps.sleep(0.1)   # delay for slow IOC

        msg = f"Setting Controller Temperature to {set_point:.2f} C"
        print(msg)
        spec_comment(msg)
        
        if wait:
            yield from self.wait_until_settled(
                timeout=timeout, 
                timeout_fail=timeout_fail)

    def wait_until_settled(self, timeout=None, timeout_fail=False):
        # see: https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python
        t0 = time.time()
        _st = DeviceStatus(self.temperature)
        started = False

        def changing_cb(value, timestamp, **kwargs):
            if started and self.settled():
                _st._finished(success=True)

        token = self.temperature.subscribe(changing_cb)
        started = True
        
        report = 0
        while not _st.done:
            elapsed = time.time() - t0
            if timeout is not None and elapsed > timeout:
                _st._finished(success=False)
                msg = f"Temperature Controller Timeout after {elapsed:.2f}s"
                msg += f", target {self.set_limit.value:.2f}C"
                msg += f", now {self.temperature.get():.2f}C"
                # msg += f", status={_st}"
                print(msg)
                if timeout_fail:
                    raise TimeoutError(msg)
                continue
            if elapsed >= report:
                report += self.report_interval
                msg = f"Waiting {elapsed:.1f}s"
                msg += f" to reach {self.set_limit.value:.2f}C"
                msg += f", now {self.temperature.get():.2f}C"
                print(msg)
            yield from bps.sleep(0.02)
        self.record_temperature()
        elapsed = time.time() - t0
        print(f"Total time: {elapsed:.3f}s, settled:{_st.success}")
        self.temperature.unsubscribe(token)

# calcout = Calcout("sky:userCalcOut9", name="calcout")
# controller = Controller("sky:userCalcOut9", name="controller")

def tester():
    # config a calcout record as a pseudo controller
    calcout.desc.put("userCalcOut9")
    calcout.calc.put("A*B+(1-B)*C")
    calcout.inpa.put("sky:userCalcOut9.VAL")
    calcout.b.put(0.5)
    calcout.c.put(0)
    calcout.d.put(0.05)
    calcout.scan.put("1 second")

    controller.wait_until_settled(timeout=10)

    controller.record_temperature()
    controller.settled()
    
    def test_plan():
        yield from controller.set_temperature(25, timeout=10)
        controller.report_interval = 1.1
        yield from controller.set_temperature(0, timeout=4)
    
    RE(test_plan())
