
print(__file__)

"""code that will become part of apstools"""

def dictionary_table(dictionary, fmt="simple"):
    """
    return a text table from ``dictionary``
    
    PARAMETERS
    
    dictionary : dict
        Python dictionary
    fmt : str
        Any of the format names provided by 
        `spec2nexus <https://pyresttable.readthedocs.io/en/latest/examples/index.html#examples>`_
        One of these: ``simple | plain | grid | complex | markdown | list-table | html``
        
        default: ``simple``
    
    RETURNS

    table : str or `None`
        multiline text table with dictionary contents in chosen format
        or ``None`` if dictionary has no contents
    
    EXAMPLE::

        In [8]: RE.md                                                                                                               
        Out[8]: {'login_id': 'jemian:wow.aps.anl.gov', 'beamline_id': 'developer', 'proposal_id': None, 'pid': 19072, 'scan_id': 10, 'version': {'bluesky': '1.5.2', 'ophyd': '1.3.3', 'apstools': '1.1.5', 'epics': '3.3.3'}}
        In [9]: print(dictionary_table(RE.md))                                                                                      
        =========== =============================================================================
        key         value                                                                        
        =========== =============================================================================
        beamline_id developer                                                                    
        login_id    jemian:wow.aps.anl.gov                                                       
        pid         19072                                                                        
        proposal_id None                                                                         
        scan_id     10                                                                           
        version     {'bluesky': '1.5.2', 'ophyd': '1.3.3', 'apstools': '1.1.5', 'epics': '3.3.3'}
        =========== =============================================================================
    """
    if len(dictionary) == 0:
        return
    _t = pyRestTable.Table()
    _t.addLabel("key")
    _t.addLabel("value")
    for k, v in sorted(dictionary.items()):
        _t.addRow((k, str(v)))
    return _t.reST(fmt=fmt)


def print_RE_md(dictionary=None, fmt="simple"):
    """
    custom print the RunEngine metadata in a table
    
    EXAMPLE::

        In [4]: print_RE_md()                                                                                                       
        RunEngine metadata dictionary:
        ======================== ===================================
        key                      value                              
        ======================== ===================================
        EPICS_CA_MAX_ARRAY_BYTES 1280000                            
        EPICS_HOST_ARCH          linux-x86_64                       
        beamline_id              APS USAXS 9-ID-C                   
        login_id                 usaxs:usaxscontrol.xray.aps.anl.gov
        pid                      67933                              
        proposal_id              testing Bluesky installation       
        scan_id                  0                                  
        versions                 ======== =====                     
                                 key      value                     
                                 ======== =====                     
                                 apstools 1.1.3                     
                                 bluesky  1.5.2                     
                                 epics    3.3.1                     
                                 ophyd    1.3.3                     
                                 ======== =====                     
        ======================== ===================================
    
    """
    global RE
    dictionary = dictionary or RE.md
    md = dict(dictionary)   # copy of input for editing
    v = dictionary_table(md["versions"], fmt=fmt)   # sub-table
    md["versions"] = str(v).rstrip()
    print("RunEngine metadata dictionary:")
    print(dictionary_table(md, fmt=fmt))
