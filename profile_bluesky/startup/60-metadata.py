print(__file__)

from datetime import datetime

# Set up default metadata

RE.md['beamline_id'] = 'Linux Mint VM7'
RE.md['proposal_id'] = 'testing'
RE.md['pid'] = os.getpid()

HOSTNAME = socket.gethostname() or 'localhost' 
USERNAME = getpass.getuser() or 'synApps_xxx_user' 
RE.md['login_id'] = USERNAME + '@' + HOSTNAME
RE.md['versions'] = {}
RE.md['versions']['bluesky'] = bluesky.__version__
RE.md['versions']['ophyd'] = ophyd.__version__
from apstools import __version__ as apstools_version
RE.md['versions']['apstools'] = apstools_version
del apstools_version
RE.md['versions']['epics'] = epics.__version__

print_RE_md()
