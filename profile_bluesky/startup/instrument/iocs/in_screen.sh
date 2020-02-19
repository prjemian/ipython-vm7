#!/bin/bash

# in_screen.sh

export BASE=$(dirname $0)
# export CAGET=/usr/local/epics/base/bin/linux-x86_64/caget

/usr/bin/screen -d -m -S IOC_registers -h 5000 ${BASE}/run_ioc.sh

echo `screen -ls`

# Q: Is softIoc available?
# 
# of these:
# (base) prjemian@ookhd:~/.ipython$ locate softIoc | grep /bin/
# /home/prjemian/Apps/miniconda3/envs/epics/epics/bin/linux-x86_64/softIoc
# /home/prjemian/Apps/miniconda3/pkgs/epics-base-3.15.6-he1b5a44_0/epics/bin/linux-x86_64/softIoc
# /home/prjemian/Apps/miniconda3/pkgs/epics-base-7.0.3.1-pl526_1/bin/softIoc
# /home/prjemian/Apps/miniconda3/pkgs/epics-base-7.0.3.1-pl526_1/bin/softIocPVA
# /home/prjemian/Apps/miniconda3/pkgs/epics-base-7.0.3.1-pl526_1/opt/epics/bin/linux-x86_64/softIoc
# /home/prjemian/Apps/miniconda3/pkgs/epics-base-7.0.3.1-pl526_1/opt/epics/bin/linux-x86_64/softIocPVA
#
# this one works: epics-base-3.15.6-he1b5a44_0
# (same as /home/prjemian/Apps/miniconda3/envs/epics/epics/bin/linux-x86_64/softIoc)
# 
# the others have problems:
# (base) prjemian@ookhd:~/.ipython$ /home/prjemian/Apps/miniconda3/pkgs/epics-base-7.0.3.1-pl526_1/bin/softIoc
# /home/prjemian/Apps/miniconda3/pkgs/epics-base-7.0.3.1-pl526_1/bin/softIoc: error while loading shared libraries: libdbRecStd.so.3.17.0: cannot open shared object file: No such file or directory
# (base) prjemian@ookhd:~/.ipython$ /home/prjemian/Apps/miniconda3/pkgs/epics-base-7.0.3.1-pl526_1/bin/softIocPVA
# /home/prjemian/Apps/miniconda3/pkgs/epics-base-7.0.3.1-pl526_1/bin/softIocPVA: error while loading shared libraries: libqsrv.so.1.1: cannot open shared object file: No such file or directory
