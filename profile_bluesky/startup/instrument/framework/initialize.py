"""
initialize the bluesky framework
"""

__all__ = [
    "bec",
    "bp",
    "bpp",
    "bps",
    "BS_CATALOG_NAME",
    "callback_db",
    "db",
    "np",
    "peaks",
    "RE",
    "sd",
    "summarize_plan",
]

from ..session_logs import logger

logger.info(__file__)

from bluesky import RunEngine
from bluesky import SupplementalData
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.callbacks.broker import verify_files_saved
from bluesky.magics import BlueskyMagics
from bluesky.simulators import summarize_plan
from bluesky.utils import get_history
from bluesky.utils import PersistentDict
from bluesky.utils import ProgressBarManager
from bluesky.utils import ts_msg_hook
from IPython import get_ipython
from ophyd.signal import EpicsSignalBase
import databroker
import ophyd
import os
import sys

# convenience imports
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
import numpy as np


# BS_CATALOG_NAME = "mongodb_config"
BS_CATALOG_NAME = "bs2021"


def get_md_path():
    md_dir_name = "Bluesky_RunEngine_md"
    if os.environ == "win32":
        home = os.environ["LOCALAPPDATA"]
        path = os.path.join(home, md_dir_name)
    else:  # at least on "linux"
        home = os.environ["HOME"]
        path = os.path.join(home, ".config", md_dir_name)
    return path


# check if we need to transition from SQLite-backed historydict
old_md = None
md_path = get_md_path()
if not os.path.exists(md_path):
    logger.info(
        "New directory to store RE.md between sessions: %s", md_path
    )
    os.makedirs(md_path)
    from bluesky.utils import get_history

    old_md = get_history()

# Set up a RunEngine and use metadata backed PersistentDict
RE = RunEngine({})
RE.md = PersistentDict(md_path)
if old_md is not None:
    logger.info("migrating RE.md storage to PersistentDict")
    RE.md.update(old_md)

# keep track of callback subscriptions
callback_db = {}

# Connect with mongodb
# db = databroker.Broker.named('mongodb_config')
db = databroker.catalog[BS_CATALOG_NAME]

# Subscribe metadatastore to documents.
# If this is removed, data is not saved to metadatastore.
callback_db["db"] = RE.subscribe(db.v1.insert)

# Set up SupplementalData.
sd = SupplementalData()
RE.preprocessors.append(sd)

# Add a progress bar.
pbar_manager = ProgressBarManager()
RE.waiting_hook = pbar_manager

# Register bluesky IPython magics.
get_ipython().register_magics(BlueskyMagics)

# Set up the BestEffortCallback.
bec = BestEffortCallback()
callback_db["bec"] = RE.subscribe(bec)
peaks = bec.peaks  # just as alias for less typing
bec.disable_baseline()

# uncomment: Verify that files saved & print confirmation message.
# _sub = RE.subscribe(post_run(verify_files_saved), 'stop')
# callback_db['post_run_verify'] = _sub


# Uncomment enable verbose debugging messages.
# ophyd.logger.setLevel(logging.DEBUG)

# diagnostics
# RE.msg_hook = ts_msg_hook

# set default timeout for all EpicsSignal connections & communications
if hasattr(EpicsSignalBase, "set_defaults"):
    # ophyd 1.6.0+
    EpicsSignalBase.set_defaults(
        auto_monitor=True,
        connection_timeout=5,
        timeout=10,
        write_timeout=5,
    )
else:
    EpicsSignalBase.set_default_timeout(
        connection_timeout=5, timeout=10,
    )
