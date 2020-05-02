
"""
example plan to find the peak of noisy v. m1
"""

__all__ = [
    'example_findpeak',
]

from ..session_logs import logger
logger.info(__file__)

import bluesky.plans as bp
import pyRestTable
from ..framework import bec, RE
from ..devices import noisy, m1


def example_findpeak(number_of_scans=3, number_of_points=23):
    """
    show simple peak finding by repeated scans with refinement

    basically::

        RE(bp.scan([noisy], m1, -2.1, 2.1, 23))

        fwhm=peaks["fwhm"]["noisy"]
        m1.move(peaks["cen"]["noisy"])
        RE(bp.rel_scan([noisy], m1, -fwhm, fwhm, 23))

        fwhm=peaks["fwhm"]["noisy"]
        m1.move(peaks["cen"]["noisy"])
        RE(bp.rel_scan([noisy], m1, -fwhm, fwhm, 23))
    """
    fwhm = 1.1
    cen = 0
    results = []
    for _again in range(number_of_scans):
        m1.move(cen)
        yield from bp.rel_scan([noisy], m1, -fwhm, fwhm, number_of_points)
        if "noisy" not in bec.peaks["fwhm"]:
            logger.error("no data in `bec.peaks`, end of these scans")
            break
        fwhm = bec.peaks["fwhm"]["noisy"]
        cen = bec.peaks["cen"]["noisy"]
        results.append((RE.md["scan_id"], cen, fwhm))
    
    tbl = pyRestTable.Table()
    tbl.labels = "scan_id center FWHM".split()
    for row in results:
        tbl.addRow(row)
    logger.info(tbl)
