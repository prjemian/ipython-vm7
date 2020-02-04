logger.info(__file__)

"""the motors"""

m1 = EpicsMotor('sky:m1', name='m1', labels=("motor",))
m2 = EpicsMotor('sky:m2', name='m2', labels=("motor",))
m3 = EpicsMotor('sky:m3', name='m3', labels=("motor",))
m4 = EpicsMotor('sky:m4', name='m4', labels=("motor",))
m5 = EpicsMotor('sky:m5', name='m5', labels=("motor",))
m6 = EpicsMotor('sky:m6', name='m6', labels=("motor",))
m7 = EpicsMotor('sky:m7', name='m7', labels=("motor",))
m8 = EpicsMotor('sky:m8', name='m8', labels=("motor",))

m16 = EpicsMotor('sky:m16', name='m16', labels=("motor",))

for m in (m1, m2, m3, m4, m5, m6, m7, m8, m16):
    epics.caput(m.prefix + ".SREV", 8000)
del m
