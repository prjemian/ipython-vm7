
"""
area detectors: ADSimDetector
"""

__all__ = [
    'adsimdet',
    # 'altsimdet',
]

import apstools.devices
from ophyd import Component
from ophyd.areadetector import EpicsSignalWithRBV
from ophyd.areadetector import ADComponent
from ophyd.areadetector import HDF5Plugin
from ophyd.areadetector import ImagePlugin
from ophyd.areadetector import AreaDetector
from ophyd.areadetector import SimDetectorCam
from ophyd.areadetector import SingleTrigger
from ophyd.areadetector import TIFFPlugin
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from ophyd.areadetector.filestore_mixins import FileStoreIterativeWrite
from ophyd.areadetector.filestore_mixins import FileStoreTIFFIterativeWrite

from ..session_logs import logger
logger.info(__file__)


DATABROKER_ROOT_PATH = "/"

# note: AD path MUST, must, MUST have trailing "/"!!!
#  ...and... start with the same path defined in root (above)

# path as seen by detector IOC
WRITE_HDF5_FILE_PATH = "/tmp/simdet/%Y/%m/%d/"

# path as seen by databroker
READ_HDF5_FILE_PATH = WRITE_HDF5_FILE_PATH


class MyHDF5Plugin(HDF5Plugin, FileStoreHDF5IterativeWrite):
    create_directory_depth = Component(EpicsSignalWithRBV, suffix="CreateDirectory")
    array_callbacks = Component(EpicsSignalWithRBV, suffix="ArrayCallbacks")

    pool_max_buffers = None
    file_number_sync = None
    file_number_write = None

class MyTIFFPlugin(TIFFPlugin, FileStoreTIFFIterativeWrite):
    # create_directory_depth = Component(EpicsSignalWithRBV, suffix="CreateDirectory")

    pool_max_buffers = None
    file_number_sync = None
    file_number_write = None

class MyCam(SimDetectorCam):
    pool_max_buffers = None

class MyImagePlugin(ImagePlugin):
    pool_max_buffers = None


class MySingleTriggerSimDetector(SingleTrigger, AreaDetector):

    cam = ADComponent(MyCam, suffix="cam1:")
    image = Component(MyImagePlugin, suffix="image1:")
    hdf1 = ADComponent(
        MyHDF5Plugin,
        suffix='HDF1:',
        root=DATABROKER_ROOT_PATH,
        write_path_template = WRITE_HDF5_FILE_PATH,
    )
    tiff1 = Component(
        MyTIFFPlugin,
        suffix='TIFF1:',
        write_path_template = WRITE_HDF5_FILE_PATH,
    )

class myHdf5EpicsIterativeWriter(
    apstools.devices.AD_EpicsHdf5FileName,
    FileStoreIterativeWrite): pass
class myHDF5FileNames(HDF5Plugin, myHdf5EpicsIterativeWriter): pass
class EpicsDefinesHDF5FileNames(HDF5Plugin, myHdf5EpicsIterativeWriter):
    create_directory_depth = Component(EpicsSignalWithRBV, suffix="CreateDirectory")


class MyRenegadeSimDetector(SingleTrigger, AreaDetector):

    cam = ADComponent(MyCam, suffix="cam1:")
    image = ADComponent(MyImagePlugin, suffix="image1:")
    hdf1 = ADComponent(
        EpicsDefinesHDF5FileNames,
        suffix = "HDF1:",
        root = DATABROKER_ROOT_PATH,
        write_path_template = WRITE_HDF5_FILE_PATH,
        # read_path_template = READ_HDF5_FILE_PATH,
        )


_ad_prefix = "adsky:"     # IOC prefix

try:
    # bluesky chooses file names with this detector
    adsimdet = MySingleTriggerSimDetector(_ad_prefix, name='adsimdet')
    adsimdet.read_attrs.append("hdf1")
    if adsimdet.hdf1.create_directory_depth.get() == 0:
        # probably not set, so let's set it now to some default
        adsimdet.hdf1.create_directory_depth.put(-5)
except TimeoutError:
    logger.error(f"Could not connect {_ad_prefix} sim detector as 'adsimdet'")

# try:
#     # EPICS chooses file names with this detector
#     altsimdet = MyRenegadeSimDetector(_ad_prefix, name='altsimdet')
#     altsimdet.read_attrs.append("hdf1")
#     if altsimdet.hdf1.create_directory_depth.get() == 0:
#         # set it now to some default
#         altsimdet.hdf1.create_directory_depth.put(-5)
#     altsimdet.hdf1.file_path.put(WRITE_HDF5_FILE_PATH)
#     altsimdet.hdf1.file_name.put("navy")
#     altsimdet.hdf1.file_number.put(101)
#     altsimdet.hdf1.array_counter.put(altsimdet.hdf1.file_number.get())

# except TimeoutError:
#     logger.error(f"Could not connect {_ad_prefix} sim detector as 'altsimdet'")
