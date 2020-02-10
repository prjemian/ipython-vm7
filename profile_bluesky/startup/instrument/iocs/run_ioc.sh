#!/bin/bash

# in_screen.sh

export BASE=$(dirname $0)
# export SOFT_IOC=/usr/local/epics/base-7.0.2/bin/linux-x86_64/softIoc
export SOFT_IOC=/usr/local/epics/base/bin/linux-x86_64/softIoc

${SOFT_IOC} -d ${BASE}/registers.db
