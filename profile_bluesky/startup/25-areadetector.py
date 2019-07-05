print(__file__)

"""area detectors: ADSimDetector"""

from ophyd.areadetector import TIFFPlugin
from ophyd.areadetector.filestore_mixins import FileStoreTIFFIterativeWrite


class MyHDF5Plugin(HDF5Plugin, FileStoreHDF5IterativeWrite):
    create_directory_depth = Component(EpicsSignalWithRBV, suffix="CreateDirectory")
    # ...

class MyTIFFPlugin(TIFFPlugin, FileStoreTIFFIterativeWrite):
    # create_directory_depth = Component(EpicsSignalWithRBV, suffix="CreateDirectory")
    ...


class MySingleTriggerSimDetector(SingleTrigger, SimDetector): 
       
    image = Component(ImagePlugin, suffix="image1:")
    hdf1 = Component(
        MyHDF5Plugin,
        suffix='HDF1:', 
        root='/',                               # for databroker
        
        # note: path MUST, must, MUST have trailing "/"!!!
        #  ...and... start with the same path defined in root (above)
        write_path_template="/tmp/simdet/%Y/%m/%d/",    # for EPICS AD
    )
    tiff1 = Component(
        MyTIFFPlugin,
        suffix='TIFF1:', 
        write_path_template="/tmp/simdet/%Y/%m/%d/",    # for EPICS AD
    )


_ad_prefix = "vm7SIM1:"		# IOC prefix
try:
    adsimdet = MySingleTriggerSimDetector(_ad_prefix, name='adsimdet')
    adsimdet.read_attrs.append("hdf1")
    if adsimdet.hdf1.create_directory_depth.value == 0:
        # probably not set, so let's set it now to some default
        adsimdet.hdf1.create_directory_depth.put(-5)
except TimeoutError:
    print(f"Could not connect {_ad_prefix} sim detector")
