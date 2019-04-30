print(__file__)

"""local, custom Device definitions"""

from ophyd.ophydobj import Kind

class ScalerCH_Local(ScalerCH):
    """
    local patch waiting on https://github.com/NSLS-II/ophyd/issues/714
    """
    
    def select_channels(self, chan_names):
        '''
        Select channels based on the EPICS name PV

        Parameters
        ----------
        chan_names : Iterable[str] or None
            The names (as reported by the channel.chname signal)
            of the channels to select.
            If *None*, select all channels named in the EPICS scaler.
        '''
        self.match_names()
        name_map = {}
        for s in self.channels.component_names:
            scaler_channel = getattr(self.channels, s)
            nm = scaler_channel.s.name  # as defined in self.match_names()
            if len(nm) > 0:
                name_map[nm] = s

        if chan_names is None:
            chan_names = name_map.keys()

        read_attrs = ['chan01']  # always include time
        for ch in chan_names:
            try:
                read_attrs.append(name_map[ch])
            except KeyError:
                raise RuntimeError("The channel {} is not configured "
                                   "on the scaler.  The named channels are "
                                   "{}".format(ch, tuple(name_map)))
        self.channels.kind = Kind.normal
        self.channels.read_attrs = list(read_attrs)
        self.channels.configuration_attrs = list(read_attrs)
        for ch in read_attrs[1:]:
            getattr(self.channels, ch).s.kind = Kind.hinted
