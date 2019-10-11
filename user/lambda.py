# get all the symbols from the IPython shell
import IPython
globals().update(IPython.get_ipython().user_ns)
logger.info(__file__)

DATABROKER_ROOT_PATH = "/"
# path as seen by detector IOC
WRITE_HDF5_FILE_PATH = "/tmp/simdet/%Y/%m/%d/"
# path as seen by databroker
READ_HDF5_FILE_PATH = WRITE_HDF5_FILE_PATH


from ophyd.device import Staged

class MyLambdaSimDetector(SingleTrigger, SimDetector): 
       
    image = Component(ImagePlugin, suffix="image1:")
    hdf1 = ADComponent(
        MyHDF5Plugin,
        suffix='HDF1:', 
        root=DATABROKER_ROOT_PATH,
        write_path_template = WRITE_HDF5_FILE_PATH,
    )
    # delayed = Component(Signal, value=False)
    # delay_s = 2

    # # ophyd.areadetector.trigger_mixins.SingleTrigger().trigger()
    # def trigger(self):
    #     "Trigger one acquisition."
    #     if self._staged != Staged.yes:
    #         raise RuntimeError("This detector is not ready to trigger."
    #                            "Call the stage() method before triggering.")

    #     # trigger_mixins.ADTriggerStatus
    #     # compares device.cam.  array_counter  &  num_images
    #     self._status = self._status_type(self)
    #     self.wait_status = DeviceStatus(self)

    #     @APS_utils.run_in_thread
    #     def delay():
    #         if self.delay_s > 0:
    #             # the plugin is usually slower than acquisition
    #             self.delayed.put(True)
    #             time.sleep(self.delay_s)
    #             self.delayed.put(True)
    #         while not self._status.done:
    #             # just in case acquisition lags our delay
    #             time.sleep(0.01)
    #         self.wait_status._finished()

    #     def closure(value,old_value,**kwargs):
    #         if not value and old_value:
    #             self.delayed.clear_sub(closure)
        
    #     delay()
    #     self.delayed.subscribe(closure)
    #     self._acquisition_signal.put(1, wait=False)
    #     self.dispatch(self._image_name, time.time())
    #     # return self._status
    #     return self.wait_status


_ad_prefix = "adsky:"     # IOC prefix

adlambda = MyLambdaSimDetector(
    _ad_prefix, 
    name='adlambda', 
    labels=["area_detector", "lambda"]
    )
adlambda.read_attrs.append("hdf1")
if adlambda.hdf1.create_directory_depth.value == 0:
    # probably not set, so let's set it now to some default
    adlambda.hdf1.create_directory_depth.put(-5)

if adlambda.image.enable.value in (0, "Disable"):
    # detector IOC is not configured yet
    adlambda.image.enable.put("Enable")
    adlambda.hdf1.enable.put("Enable")
    adlambda.hdf1.file_name.put("bluesky")
    adlambda.hdf1.file_path.put("/tmp/simdet/")
    adlambda.hdf1.file_template.put("%s%s_%3.3d.h5")
    adlambda.hdf1.file_number.put(101)
    adlambda.hdf1.auto_save.put("Yes")
    adlambda.hdf1.auto_increment.put("Yes")
    # adlambda.hdf1.blocking_callbacks.put("Yes")
    adlambda.cam.image_mode.put("Single")
    # adlambda.cam.bin_x.put(17)
    # adlambda.cam.bin_y.put(29)

    # pump a few frames through the plugins
    for i in range(3):
        adlambda.hdf1.capture.put(1)
        adlambda.cam.acquire.put(1)
        time.sleep(0.1)

def shot(t=0.001, n=20):
    adlambda.cam.stage_sigs["acquire_time"] = t
    adlambda.cam.stage_sigs["acquire_period"] = t  # + 0.001
    adlambda.cam.stage_sigs["num_images"] = n
    adlambda.hdf1.stage_sigs["num_capture"] = n
    adlambda.hdf1.stage_sigs["blocking_callbacks"] = "No"
    adlambda.hdf1.stage_sigs["array_callbacks"] = 1
    yield from bp.count([adlambda])
