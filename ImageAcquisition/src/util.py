import PySpin

def SetExposureTime(cam, exposure_time_to_set):
    # unit of exposure_time_to_set is microseconds

    # Step 1: Disable ExposureAuto:
    if cam.ExposureAuto.GetAccessMode() != PySpin.RW:
        print('Unable to disable automatic exposure. Aborting...')
        return False
    cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
    print('Automatic exposure disabled...')

    # Step 2: Set ExposureTime:
    if cam.ExposureTime.GetAccessMode() != PySpin.RW:
        print('Unable to set exposure time. Aborting...')
        return False
    # Ensure desired exposure time does not exceed the maximum
    # exposure_time_to_set = 2000000.0
    exposure_time_to_set = min(cam.ExposureTime.GetMax(), exposure_time_to_set)
    cam.ExposureTime.SetValue(exposure_time_to_set)
    print('Shutter time set to %s us...\n' % exposure_time_to_set)
