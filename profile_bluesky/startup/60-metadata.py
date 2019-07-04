print(__file__)

from datetime import datetime

# Set up default metadata

RE.md['beamline_id'] = 'Linux Mint VM7'
RE.md['proposal_id'] = 'testing'
RE.md['pid'] = os.getpid()

HOSTNAME = socket.gethostname() or 'localhost' 
USERNAME = getpass.getuser() or 'synApps_xxx_user' 
RE.md['login_id'] = USERNAME + '@' + HOSTNAME

# useful diagnostic to record with all data
RE.md['versions'] = {}
RE.md['versions']['bluesky'] = bluesky.__version__
RE.md['versions']['ophyd'] = ophyd.__version__
from databroker import __version__ as db_version
RE.md['versions']['databroker'] = db_version
del db_version
from apstools import __version__ as apstools_version
RE.md['versions']['apstools'] = apstools_version
del apstools_version
RE.md['versions']['epics'] = epics.__version__
RE.md['versions']['numpy'] = np.__version__
from matplotlib import __version__ as mpl_version
from matplotlib import __version__numpy__ as mpl_np_version
RE.md['versions']['matplotlib.numpy'] = mpl_np_version
del mpl_version
del mpl_np_version
from spec2nexus import __version__ as s2n_version
RE.md['versions']['spec2nexus'] = s2n_version
del s2n_version
RE.md['versions']['pyRestTable'] = pyRestTable.__version__

print_RE_md()
