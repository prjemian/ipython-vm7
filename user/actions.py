
# get all the symbols from the IPython shell
import IPython
globals().update(IPython.get_ipython().user_ns)
logger.info(__file__)


def action1():
    APS_utils.show_ophyd_symbols()
    print(scaler.read())

def catalog():
    table = pyRestTable.Table()
    table.labels = "symbol type".split()
    for k, v in sorted(globals().items()):
        if k.startswith("_") or k in ("In",):
            continue
        table.addRow((k, type(v)))
    print(table)
