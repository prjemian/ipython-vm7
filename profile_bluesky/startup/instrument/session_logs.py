"""
configure session logging
"""

from IPython import get_ipython
import os
# pip install stdlogpj
import stdlogpj

__all__ = ['logger',]

LOG_NAME = "bluesky-session"

_log_path = os.path.join(os.getcwd(), ".logs")
if not os.path.exists(_log_path):
    os.mkdir(_log_path)
CONSOLE_IO_FILE = os.path.join(_log_path, "ipython_console.log")

# start logging console to file
# https://ipython.org/ipython-doc/3/interactive/magics.html#magic-logstart
_ipython = get_ipython()
# %logstart -o -t .ipython_console.log "rotate"
_ipython.magic(f"logstart -o -t {CONSOLE_IO_FILE} rotate")


logger = stdlogpj.standard_logging_setup(LOG_NAME, "ipython_logger")


logger.info('#'*60 + " startup")
logger.info('logging started')
logger.info(f'logging level = {logger.level}')

# logger.debug('example Debug message')
# logger.info('example Info message')
# logger.warning('example Warning message')
# logger.error('example Error message')
