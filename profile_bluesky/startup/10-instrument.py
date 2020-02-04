
import logging
from instrument.startup.console_session import *
logger = logging.getLogger(__name__)

show_ophyd_symbols()
print(print_RE_md(printing=False))
