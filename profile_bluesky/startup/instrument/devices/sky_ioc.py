
"""
details of the sky IOC from iocStats

this could/should go into apstools.devices
"""

__all__ = ["iocsky",]

from ..session_logs import logger
logger.info(__file__)

from ophyd import Component, Device, EpicsSignalRO, Signal

class IocStatsDevice(Device):

    _app_dir1 = Component(EpicsSignalRO, "APP_DIR1", kind="omitted")
    _app_dir2 = Component(EpicsSignalRO, "APP_DIR2", kind="omitted")
    _startup_script1 = Component(EpicsSignalRO, "ST_SCRIPT1", kind="omitted")
    _startup_script2 = Component(EpicsSignalRO, "ST_SCRIPT2", kind="omitted")
    access = Component(EpicsSignalRO, "ACCESS", string=True)
    application_directory = Component(Signal, value="")
    ca_client_count = Component(EpicsSignalRO, "CA_CLNT_CNT")
    ca_connection_count = Component(EpicsSignalRO, "CA_CONN_CNT")
    cpu_count = Component(EpicsSignalRO, "CPU_CNT")
    engineer = Component(EpicsSignalRO, "ENGINEER")
    epics_version = Component(EpicsSignalRO, "EPICS_VERS")
    file_descriptors_free = Component(EpicsSignalRO, "FD_FREE")
    file_descriptors_max_ = Component(EpicsSignalRO, "FD_MAX")
    heartbeat = Component(EpicsSignalRO, "HEARTBEAT")
    host_name = Component(EpicsSignalRO, "HOSTNAME")
    ioc_cpu_load = Component(EpicsSignalRO, "IOC_CPU_LOAD")
    iso8601 = Component(EpicsSignalRO, "iso8601")
    kernel_version = Component(EpicsSignalRO, "KERNEL_VERS")
    location = Component(EpicsSignalRO, "LOCATION")
    max_array_bytes = Component(EpicsSignalRO, "CA_MAX_ARRAY")
    memory_free = Component(EpicsSignalRO, "MEM_FREE")
    memory_max = Component(EpicsSignalRO, "MEM_MAX")
    memory_used = Component(EpicsSignalRO, "MEM_USED")
    memory_used_percentage = Component(Signal, value=0)
    records_count = Component(EpicsSignalRO, "RECORD_CNT")
    startup_script = Component(Signal, value="")
    startup_time = Component(EpicsSignalRO, "STARTTOD")
    suspended_task_count = Component(EpicsSignalRO, "SUSP_TASK_CNT")
    system_cpu_load = Component(EpicsSignalRO, "SYS_CPU_LOAD")
    time_of_day = Component(EpicsSignalRO, "TOD")
    timezone = Component(EpicsSignalRO, "TIMEZONE")
    uptime = Component(EpicsSignalRO, ":UPTIME")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        def ad_update(value, *args, **kwargs):
            self.application_directory.put(
                self._app_dir1.get()+self._app_dir2.get()
            )
        self._app_dir1.subscribe(ad_update)
        self._app_dir2.subscribe(ad_update)
        
        def ss_update(value, *args, **kwargs):
            self.startup_script.put(
                self._startup_script1.get()+self._startup_script2.get()
            )
        self._startup_script1.subscribe(ss_update)
        self._startup_script2.subscribe(ss_update)
        
        def mem_used_update(value, *args, **kwargs):
            self.memory_used_percentage.put(
                100 * self.memory_used.get() / self.memory_max.get()
            )
        self.memory_used.subscribe(mem_used_update)


iocsky = IocStatsDevice("sky:", name="iocsky")