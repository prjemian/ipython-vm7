

"""
"""

import apstools.synApps
from instrument.startup.framework import RE, bp, db
from instrument.devices import m1, scaler, calcouts, clock, I0, I0Mon, scint

from instrument.session_logs import logger
logger.info(__file__)

from bluesky.callbacks.fitting import PeakStats
import pyRestTable


# FIXME: looks like trouble with the call to RE.subscribe
def my_scan(count_time=1.0):
    mot = m1
    scaler.stage_sigs["preset_time"] = count_time
    scaler.stage_sigs["count_mode"] = "OneShot"

    peaky = calcouts.calcout9
    calc = calcouts.calcout10
    peaky.reset()
    calc.reset()

    md = {
        "count_time": count_time,
        "title": "monitor example",
    }

    monitored_signals = [
        calc.calculated_value,
        peaky.calculated_value,
        clock,
        I0,
        scint,
        I0Mon,
        # noisy,
    ]
    apstools.synApps.setup_incrementer_calcout(calc)
    apstools.synApps.setup_lorentzian_calcout(peaky, mot.user_readback, center=-1.4, width=0.3, scale=10)

    #@bpp.stage_decorator([calc])
    @bpp.monitor_during_decorator(monitored_signals)
    def inner():
        y_signal = peaky.calculated_value
        x_signal = mot

        ps = PeakStats(x_signal.name, y_signal.name)
        RE.subscribe(ps)    # collects data during scan     # FIXME: trouble here

        yield from bp.scan([y_signal, calc.calculated_value], x_signal, -2, 0, 41, md=md)

        tbl = pyRestTable.Table()
        tbl.labels = "PeakStats value".split()
        tbl.rows = [
            [k, ps.__getattribute__(k)] 
            for k in sorted("min max cen com fwhm".split())
            ]

        h = db[-1]
        logger.info(f"scan_id={RE.md['scan_id']}")
        logger.info(f"uid={h.start['uid']}")
        logger.info(tbl)
        calc.reset()

    return (yield from inner())
