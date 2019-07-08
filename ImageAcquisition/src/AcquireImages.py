import os
import PySpin
import time
import serial
from util import SetExposureTime

#set the exposure time to be used
exposure = 70000

#set the number of image pairs to be recorded
NUM_IMAGES = 64

#set the serial port for the Arduino controling the leds
arduino_port = '/dev/ttyUSB0'

#set the path to the folder for output images
output_folder = 'output/AcquireImages/'

arduino = serial.Serial(arduino_port, 115200, timeout=.1) #open serial port
time.sleep(2) #give the serial port time to settle
arduino.write(bytes("o", 'ASCII')) #make sure both leds are off

#set the total number of buffers to 2 for one image pair
NUM_BUFFERS = 2


def configure_trigger(nodemap):
	try:
		result = True
		print('\n*** CONFIGURING TRIGGER ***\n')

		# Ensure trigger mode is off
		#
		# *** NOTES ***
		# The trigger must be disabled in order to configure the
		# trigger source.
		trigger_mode = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerMode'))
		if not PySpin.IsAvailable(trigger_mode) or not PySpin.IsWritable(trigger_mode):
			print('Unable to disable trigger mode (node retrieval). Aborting...\n')
			return False

		trigger_mode_off = PySpin.CEnumEntryPtr(trigger_mode.GetEntryByName('Off'))
		if not PySpin.IsAvailable(trigger_mode_off) or not PySpin.IsReadable(trigger_mode_off):
			print('Unable to disable trigger mode (enum entry retrieval). Aborting...\n')
			return False

		trigger_mode.SetIntValue(trigger_mode_off.GetValue())
		print('Trigger mode disabled...')

		# Set trigger source to software
		trigger_source = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerSource'))
		if not PySpin.IsAvailable(trigger_source) or not PySpin.IsWritable(trigger_source):
			print('Unable to set trigger mode (node retrieval). Aborting...')
			return False

		trigger_source_software = PySpin.CEnumEntryPtr(trigger_source.GetEntryByName('Software'))
		if not PySpin.IsAvailable(trigger_source_software) or not PySpin.IsReadable(trigger_source_software):
			print('Unable to set trigger mode (enum entry retrieval). Aborting...')
			return False

		trigger_source.SetIntValue(trigger_source_software.GetValue())
		print('Trigger source set to software...')

		# Turn trigger mode on
		trigger_mode_on = PySpin.CEnumEntryPtr(trigger_mode.GetEntryByName('On'))
		if not PySpin.IsAvailable(trigger_mode_on) or not PySpin.IsReadable(trigger_mode_on):
			print('Unable to enable trigger mode (enum entry retrieval). Aborting...\n')
			return False

		trigger_mode.SetIntValue(trigger_mode_on.GetValue())
		print('Trigger mode turned back on...')

	except PySpin.SpinnakerException as ex:
		print('Error: %s' % ex)
		result = False

	return result

def grab_next_image_by_trigger(nodemap, mode, exposure):
	"""
	This turns on one LED, sends a trigger to the camera and turns the LED off again after the images taken
	"""
	try:
		result = True

		#turn on led
		arduino.write(bytes(mode, 'ASCII'))
		time.sleep(0.004)

		# Execute software trigger
		software_trigger_command = PySpin.CCommandPtr(nodemap.GetNode('TriggerSoftware'))
		if not PySpin.IsAvailable(software_trigger_command) or not PySpin.IsWritable(software_trigger_command):
			print('Unable to execute trigger. Aborting...\n')
			return False

		software_trigger_command.Execute()

		#turn off led
		time.sleep(0.008+(exposure/1000000))
		arduino.write(bytes(mode, 'ASCII'))

	except PySpin.SpinnakerException as ex:
		print('Error: %s' % ex)
		result = False

	return result

def reset_trigger(nodemap):
	"""
	This function returns the camera to a normal state by turning off trigger mode.
	"""
	try:
		result = True

		# Turn trigger mode back off
		#
		# *** NOTES ***
		# Once all images have been captured, turn trigger mode back off to
		# restore the camera to a clean state.
		trigger_mode = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerMode'))
		if not PySpin.IsAvailable(trigger_mode) or not PySpin.IsWritable(trigger_mode):
			print('Unable to disable trigger mode (node retrieval). Non-fatal error...\n')
			return False

		trigger_mode_off = PySpin.CEnumEntryPtr(trigger_mode.GetEntryByName('Off'))
		if not PySpin.IsAvailable(trigger_mode_off) or not PySpin.IsReadable(trigger_mode_off):
			print('Unable to disable trigger mode (enum entry retrieval). Non-fatal error...\n')
			return False

		trigger_mode.SetIntValue(trigger_mode_off.GetValue())
		print('Trigger mode disabled...\n')

	except PySpin.SpinnakerException as ex:
		print('Error: %s' % ex)
		result = False

	return result

def print_device_info(nodemap):
	"""
	This function prints the device information of the camera from the transport
	layer; please see NodeMapInfo example for more in-depth comments on printing
	device information from the nodemap.

	:param nodemap: Transport layer device nodemap from camera.
	:type nodemap: INodeMap
	:return: True if successful, False otherwise.
	:rtype: bool
	"""
	try:
		result = True
		print('\n*** DEVICE INFORMATION ***\n')

		# Retrieve and display Device Information
		node_device_information = PySpin.CCategoryPtr(nodemap.GetNode('DeviceInformation'))
		if PySpin.IsAvailable(node_device_information) and PySpin.IsReadable(node_device_information):
			features = node_device_information.GetFeatures()
			for feature in features:
				node_feature = PySpin.CValuePtr(feature)
				print('%s: %s' % (node_feature.GetName(),
								  node_feature.ToString() if PySpin.IsReadable(node_feature) else 'Node not readable'))

		else:
			print('Device control information not available.')

	except PySpin.SpinnakerException as ex:
		print('Error: %s' % ex)
		result = False

	return result

def acquire_images(cam, nodemap, nodemap_tldevice):
	"""
	This function Acquires NUM_IMAGES pairs of polarized images
	"""
	try:
		result = True
		print('\n*** IMAGE ACQUISITION ***\n')

		node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
		if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
			print('Unable to set acquisition mode to continuous (node retrieval). Aborting...')
			return False

		# Retrieve entry node from enumeration mode
		node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
		if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
				node_acquisition_mode_continuous):
			print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
			return False

		# Retrieve integer value from entry node
		acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

		# Set integer value from entry node as new value of enumeration node
		node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

		print('Acquisition mode set to continuous...')


		# Retrieve Stream Parameters device nodemap
		s_node_map = cam.GetTLStreamNodeMap()

		# Retrieve Buffer Handling Mode Information
		handling_mode = PySpin.CEnumerationPtr(s_node_map.GetNode('StreamBufferHandlingMode'))
		if not PySpin.IsAvailable(handling_mode) or not PySpin.IsWritable(handling_mode):
			print('Unable to set Buffer Handling mode (node retrieval). Aborting...\n')
			return False

		handling_mode_entry = PySpin.CEnumEntryPtr(handling_mode.GetCurrentEntry())
		if not PySpin.IsAvailable(handling_mode_entry) or not PySpin.IsReadable(handling_mode_entry):
			print('Unable to set Buffer Handling mode (Entry retrieval). Aborting...\n')
			return False

		# Set stream buffer Count Mode to manual
		stream_buffer_count_mode = PySpin.CEnumerationPtr(s_node_map.GetNode('StreamBufferCountMode'))
		if not PySpin.IsAvailable(stream_buffer_count_mode) or not PySpin.IsWritable(stream_buffer_count_mode):
			print('Unable to set Buffer Count Mode (node retrieval). Aborting...\n')
			return False

		stream_buffer_count_mode_manual = PySpin.CEnumEntryPtr(stream_buffer_count_mode.GetEntryByName('Manual'))
		if not PySpin.IsAvailable(stream_buffer_count_mode_manual) or not PySpin.IsReadable(stream_buffer_count_mode_manual):
			print('Unable to set Buffer Count Mode entry (Entry retrieval). Aborting...\n')
			return False

		stream_buffer_count_mode.SetIntValue(stream_buffer_count_mode_manual.GetValue())
		print('Stream Buffer Count Mode set to manual...')

		# Retrieve and modify Stream Buffer Count
		buffer_count = PySpin.CIntegerPtr(s_node_map.GetNode('StreamBufferCountManual'))
		if not PySpin.IsAvailable(buffer_count) or not PySpin.IsWritable(buffer_count):
			print('Unable to set Buffer Count (Integer node retrieval). Aborting...\n')
			return False

		# Display Buffer Info
		print('\nDefault Buffer Handling Mode: %s' % handling_mode_entry.GetDisplayName())
		print('Default Buffer Count: %d' % buffer_count.GetValue())
		print('Maximum Buffer Count: %d' % buffer_count.GetMax())

		buffer_count.SetValue(NUM_BUFFERS)

		print('Buffer count now set to: %d' % buffer_count.GetValue())

		handling_mode_entry = handling_mode.GetEntryByName('OldestFirst')
		handling_mode.SetIntValue(handling_mode_entry.GetValue())
		print('\n\nBuffer Handling Mode has been set to %s' % handling_mode_entry.GetDisplayName())
		
		# Begin capturing images
		cam.BeginAcquisition()


		try:
			images = []
			SetExposureTime(cam, exposure)
			time.sleep(1)
			for i in range(NUM_IMAGES):
				# Software Trigger the camera with vertically polarized LED turned on
				result &= grab_next_image_by_trigger(nodemap, 'v', exposure)
				time.sleep(0.02)
				# Software Trigger the camera with horizontally polarized LED turned on
				result &= grab_next_image_by_trigger(nodemap, 'h', exposure)
				time.sleep(0.02)
			
				#Save the two acquired images
				for loop_cnt in range (2):
					result_image = cam.GetNextImage(1000)

					if result_image.IsIncomplete():
						print('Image incomplete with image status %s ...\n' % result_image.GetImageStatus())

					if loop_cnt % 2 == 0:
						photo_mode = 'crossed'
					else:
						photo_mode = 'parallel'
					filename = output_folder + '%d-%s.jpg' % (i, photo_mode)
					
					# Save image
					result_image.Save(filename)
					
					# Release image
					result_image.Release()
					
				time.sleep(1.5)

		except PySpin.SpinnakerException as ex:
			print('Error: %s' % ex)
			if handling_mode_entry.GetSymbolic() == 'NewestOnly':
				print('Error should occur when grabbing image 1 with handling mode set to NewestOnly')
			result = False

			# End acquisition
			cam.EndAcquisition()

	except PySpin.SpinnakerException as ex:
		print('Error: %s' % ex)
		result = False

	return result

def run_single_camera(cam):
	"""
	This function acts as the body of the script
	"""
	try:
		result = True

		# Retrieve TL device nodemap and print device information
		nodemap_tldevice = cam.GetTLDeviceNodeMap()

		result &= print_device_info(nodemap_tldevice)

		# Initialize camera
		cam.Init()

		# Retrieve GenICam nodemap
		nodemap = cam.GetNodeMap()

		# Configure chunk data
		if configure_trigger(nodemap) is False:
			return False

		# Acquire images and display chunk data
		result &= acquire_images(cam, nodemap, nodemap_tldevice)

		# Reset trigger
		result &= reset_trigger(nodemap)

		# De-initialize camera
		cam.DeInit()

	except PySpin.SpinnakerException as ex:
		print('Error: %s' % ex)
		result = False

	return result

def main():
	# Since this application saves images in the current folder
	# it hast to be ensured that we have permission to write to this folder.
	# If we do not have permission, fail right away.
	try:
		test_file = open('test.txt', 'w+')
	except IOError:
		print('Unable to write to current directory. Please check permissions.')
		input('Press Enter to exit...')
		return False

	test_file.close()
	os.remove(test_file.name)

	result = True

	# Retrieve singleton reference to system object
	system = PySpin.System.GetInstance()

	# Get current library version
	version = system.GetLibraryVersion()
	print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))

	# Retrieve list of cameras from the system
	cam_list = system.GetCameras()

	num_cameras = cam_list.GetSize()

	print('Number of cameras detected: %d' % num_cameras)

	# Finish if there are no cameras
	if num_cameras == 0:
		# Clear camera list before releasing system
		cam_list.Clear()

		# Release system instance
		system.ReleaseInstance()

		print('Not enough cameras!')
		input('Done! Press Enter to exit...')
		return False

	# Run example on each camera
	for i, cam in enumerate(cam_list):
		print('\n\nRunning example for camera %d...' % i)

		result &= run_single_camera(cam)
		print('Camera %d example complete... \n' % i)

		# Release reference to camera
	del cam

	# Clear camera list before releasing system
	cam_list.Clear()

	# Release system instance
	system.ReleaseInstance()
	
	arduino.close()
	
	input('Done! Press Enter to exit...')
	return result


if __name__ == '__main__':
	main()



