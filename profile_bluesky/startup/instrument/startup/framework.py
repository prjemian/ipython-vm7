
"""
initialize the bluesky framework
"""

import logging
logger = logging.getLogger(__name__)
logger.info(__file__)

# Set up a RunEngine and use metadata backed by a sqlite file.
from bluesky import RunEngine
from bluesky.utils import get_history
RE = RunEngine(get_history())

# keep track of callback subscriptions
callback_db = {}

# Set up a Broker.
from databroker import Broker
db = Broker.named('mongodb_config')

# Subscribe metadatastore to documents.
# If this is removed, data is not saved to metadatastore.
callback_db['db'] = RE.subscribe(db.insert)

# Set up SupplementalData.
from bluesky import SupplementalData
sd = SupplementalData()
RE.preprocessors.append(sd)

# Add a progress bar.
from bluesky.utils import ProgressBarManager
pbar_manager = ProgressBarManager()
RE.waiting_hook = pbar_manager

# Register bluesky IPython magics.
from IPython import get_ipython
from bluesky.magics import BlueskyMagics
get_ipython().register_magics(BlueskyMagics)

# Set up the BestEffortCallback.
from bluesky.callbacks.best_effort import BestEffortCallback
bec = BestEffortCallback()
callback_db['bec'] = RE.subscribe(bec)
peaks = bec.peaks  # just as alias for less typing
bec.disable_baseline()

# At the end of every run, verify that files were saved and
# print a confirmation message.
from bluesky.callbacks.broker import verify_files_saved
# callback_db['post_run_verify'] = RE.subscribe(post_run(verify_files_saved), 'stop')

# Make plots update live while scans run.
from bluesky.utils import install_qt_kicker
install_qt_kicker()

# convenience imports
from bluesky.callbacks import *
from bluesky.callbacks.broker import *
# from bluesky.simulators import *
from bluesky import plans as bp
import numpy as np
