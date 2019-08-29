
"""
Ophyd support for the EPICS transform record


Public Structures

.. autosummary::
   
    ~transformRecord
    ~userTransformsDevice
"""

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     jemian@anl.gov
# :copyright: (c) 2017-2019, UChicago Argonne, LLC
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

from collections import OrderedDict
from ophyd.device import (
    Device,
    Component as Cpt,
    DynamicDeviceComponent as DDC,
    FormattedComponent as FC)
from ophyd import EpicsSignal, EpicsSignalRO

from .common_fields import EpicsRecordDeviceCommonAll
# from .. import utils as APS_utils
from apstools import utils as APS_utils


__all__ = [
    "transformRecord",
    "userTransformsDevice",
    ]


LIST_CHANNEL_LETTERS = "A B C D E F G H I J K L M N O P".split()


class transformRecordChannel(Device):
    """channel of a synApps transform record: A-P"""
    current_value = FC(EpicsSignal,         '{self.prefix}.{self._ch_letter}')
    last_value = FC(EpicsSignalRO,          '{self.prefix}.L{self._ch_letter}')
    input_pv = FC(EpicsSignal,              '{self.prefix}.INP{self._ch_letter}')
    input_pv_valid = FC(EpicsSignalRO,      '{self.prefix}.I{self._ch_letter}V')
    expression_invalid = FC(EpicsSignalRO,  '{self.prefix}.C{self._ch_letter}V')
    comment = FC(EpicsSignal,               '{self.prefix}.CMT{self._ch_letter}')
    expression = FC(EpicsSignal,            '{self.prefix}.CLC{self._ch_letter}')
    output_pv = FC(EpicsSignal,             '{self.prefix}.OUT{self._ch_letter}')
    output_pv_valid = FC(EpicsSignalRO,     '{self.prefix}.O{self._ch_letter}V')
    
    read_attrs = ["current_value"]
    
    def __init__(self, prefix, letter, **kwargs):
        self._ch_letter = letter
        super().__init__(prefix, **kwargs)

    def reset(self):
        """set all fields to default values"""
        self.comment.put(self._ch_letter.lower())
        self.input_pv.put("")
        self.expression.put("")
        self.current_value.put(0)
        self.output_pv.put("")


def _channels(channel_list):
    defn = OrderedDict()
    for chan in channel_list:
        defn[chan] = (transformRecordChannel, '', {'letter': chan})
    return defn


class transformRecord(EpicsRecordDeviceCommonAll):
    """
    EPICS transform record support in ophyd
    
    :see: https://htmlpreview.github.io/?https://raw.githubusercontent.com/epics-modules/calc/R3-6-1/documentation/transformRecord.html#Fields
    """
    units = Cpt(EpicsSignal, ".EGU")
    precision = Cpt(EpicsSignal, ".PREC")
    version = Cpt(EpicsSignalRO, ".VERS")

    calc_option = Cpt(EpicsSignal, ".COPT")
    invalid_link_action = Cpt(EpicsSignalRO, ".IVLA")
    input_bitmap = Cpt(EpicsSignalRO, ".MAP")

    read_attrs = APS_utils.itemizer("channels.%s", LIST_CHANNEL_LETTERS)
    hints = {'fields': read_attrs}

    channels = DDC(_channels(LIST_CHANNEL_LETTERS))
    
    def reset(self):
        """set all fields to default values"""
        self.scanning_rate.put("Passive")
        self.description.put(self.description.pvname.split(".")[0])
        self.units.put("")
        self.calc_option.put(0)
        self.precision.put("3")
        self.forward_link.put("")
        for letter in self.channels.read_attrs:
            channel = getattr(self.channels, letter)
            if isinstance(channel, transformRecordChannel):
                channel.reset()
        self.hints = {'fields': ["channels.%s" % c for c in LIST_CHANNEL_LETTERS]}
        self.read_attrs = ["channels.%s" % c for c in LIST_CHANNEL_LETTERS]


class userTransformsDevice(Device):
    """
    synApps XXX IOC setup of userTransforms: $(P):userTran$(N)

    .. autosummary::
       
        ~reset

    """

    enable = Cpt(EpicsSignal, 'userTranEnable')
    transform1 = Cpt(transformRecord, 'userTran1')
    transform2 = Cpt(transformRecord, 'userTran2')
    transform3 = Cpt(transformRecord, 'userTran3')
    transform4 = Cpt(transformRecord, 'userTran4')
    transform5 = Cpt(transformRecord, 'userTran5')
    transform6 = Cpt(transformRecord, 'userTran6')
    transform7 = Cpt(transformRecord, 'userTran7')
    transform8 = Cpt(transformRecord, 'userTran8')
    transform9 = Cpt(transformRecord, 'userTran9')
    transform10 = Cpt(transformRecord, 'userTran10')

    def reset(self):
        """set all fields to default values"""
        self.transform1.reset()
        self.transform2.reset()
        self.transform3.reset()
        self.transform4.reset()
        self.transform5.reset()
        self.transform6.reset()
        self.transform7.reset()
        self.transform8.reset()
        self.transform9.reset()
        self.transform10.reset()
        self.read_attrs = ["transform%d" % (c+1) for c in range(10)]
        self.read_attrs.insert(0, "enable")
