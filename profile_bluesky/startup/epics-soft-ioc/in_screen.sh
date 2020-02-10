#!/bin/bash

# in_screen.sh
export BASE=/home/mintadmin/.ipython/profile_bluesky/startup/epics-soft-ioc
/usr/bin/screen -dm -S IOC_registers -h 5000 ${BASE}/run_ioc.sh
