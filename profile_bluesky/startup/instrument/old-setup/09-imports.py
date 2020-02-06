logger.info(__file__)

"""gather all the imports here"""


import collections
import datetime
from enum import Enum
import getpass 
import IPython
import itertools
import os
import pyRestTable
import socket
import spec2nexus
import time
import uuid

from ophyd import Component, Device, DeviceStatus, Signal
from ophyd import EpicsMotor, MotorBundle, PseudoPositioner, PseudoSingle, SoftPositioner

from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV
from ophyd import FormattedComponent 
from ophyd.scaler import ScalerCH, ScalerChannel
from ophyd.sim import SynSignal

# area detector support (ADSimDetector)
from ophyd import SingleTrigger, SimDetector
from ophyd import HDF5Plugin, ImagePlugin
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite

import apstools.callbacks as APS_callbacks
import apstools.devices as APS_devices
import apstools.filewriters as APS_filewriters
import apstools.plans as APS_plans
import apstools.synApps as APS_synApps
import apstools.suspenders as APS_suspenders
import apstools.utils as APS_utils

# import specific methods by name, we need to customize them sometimes
from apstools.devices import SimulatedApsPssShutterWithStatus
from apstools.filewriters import SpecWriterCallback, spec_comment
from apstools.utils import print_RE_md
from apstools.utils import show_ophyd_symbols

sys.path.append(os.path.join(IPython.paths.get_ipython_dir(), "user"))
