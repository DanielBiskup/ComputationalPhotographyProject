# FindGoodExposureTime

One of our cameras didn't allow us to set ExposureTime. The description of which
in SpinView is:

> Exposure time in microseconds when Exposure Mode is Timed and ExposureAuto is Off.

Thus we probably have to set ExposureAuto to Off before setting ExposureTime.

You do that with:
```py
if cam.ExposureAuto.GetAccessMode() != PySpin.RW:
    print('Unable to disable automatic exposure. Aborting...')
    return False
cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
print('Automatic exposure disabled...')
```
then set the exposure time with:
```py
if cam.ExposureTime.GetAccessMode() != PySpin.RW:
  print('Unable to set exposure time. Aborting...')
  return False

# Ensure desired exposure time does not exceed the maximum
exposure_time_to_set = 2000000.0
exposure_time_to_set = min(cam.ExposureTime.GetMax(), exposure_time_to_set)
cam.ExposureTime.SetValue(exposure_time_to_set)
print('Shutter time set to %s us...\n' % exposure_time_to_set)
```
