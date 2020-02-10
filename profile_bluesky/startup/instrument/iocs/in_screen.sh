#!/bin/bash

# in_screen.sh

export BASE=$(dirname $0)
export CAGET=/usr/local/epics/base/bin/linux-x86_64/caget

/usr/bin/screen -d -m -S IOC_registers -h 5000 ${BASE}/run_ioc.sh

echo `screen -ls`
