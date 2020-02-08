
"""
"""

__all__ = ['object_explorer',]

from ophyd import Device
from ophyd.signal import EpicsSignalBase
import pyRestTable

def get_child(obj, nm):
    try:
        child = getattr(obj, nm)
        return child
    except TimeoutError:
        print(f"timeout: {obj.name}_{nm}")
        return "TIMEOUT"
    print(f"None: {obj.name}_{nm}")


def miner(obj):
    # import pdb; pdb.set_trace()
    if isinstance(obj, EpicsSignalBase):
        return [obj]
    elif isinstance(obj, Device):
        items = []
        for nm in obj.component_names:
            child = get_child(obj, nm)
            if child in (None, "TIMEOUT"):
                continue
            result = miner(child)
            if result is not None:
                items.extend(result)
        return items


def pv_ref(obj):
    if isinstance(obj, EpicsSignalBase):
        return obj.pvname
    elif isinstance(obj, Device):
        return obj.prefix


def dotted_name(obj):
    """Return the dotted name"""
    names = []
    while obj.parent is not None:
        names.append(obj.attr_name)
        obj = obj.parent
    names.append(obj.name)
    return '.'.join(names[::-1])


def object_explorer(obj):
    """
    print the contents of obj
    """
    t = pyRestTable.Table()
    t.addLabel("name")
    t.addLabel("PV reference")
    t.addLabel("value")
    items = miner(obj)
    print(len(items))
    for item in items:
        t.addRow((dotted_name(item), pv_ref(item), item.get()))
    print(t)
    return t
