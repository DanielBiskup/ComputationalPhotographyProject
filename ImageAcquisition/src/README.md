# Scripts for acquiring images
Our scripts for image acquisition are:

* `AcquireImages.py`
* `FindGoodExposureTime.py`
* `util.py`

## AcquireImages.py
The script used to capture datasets. It required custom hardware, i.e. our arduino controlling two LEDs attached to a beam splitter.

## FindGoodExposureTime.py
This script is intendet to help find a good exposure time.
It takes a few photos with different exposure times. You can set the exposure
times used in the `exposrues` array.

## util.py
Provides the `SetExposureTime` function.

### Set Expose Time
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

### Gray images / Color images
It might seem random, that sometimes images captured are gray and sometimes they
have color. That's because the cameras configuration is actually saved on the
camera as long as it's connected to the computer.

Thus, we found, that after plugging in the camera into the USB slot, before
using any of our scripts to capture images, we have to open the SpinView
application, and set the capture mode to *continuous*, click *capture*, stop the
capture again, and close SpinView.

This apparently sets some sane default parameters on the camera, which we assume
to be set in our scripts. Most noticeably the images will now be RGB instread of
gray.
