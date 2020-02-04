
"""
support a .ipython/user directory for user files
"""

import IPython.paths
import logging
import os
import sys

logger = logging.getLogger(__name__)
logger.info(__file__)

user_dir = os.path.join(
        IPython.paths.get_ipython_dir(), 
        "user"
    )
sys.path.append(user_dir)

logger.info(f"User code directory: {user_dir}")
del user_dir
