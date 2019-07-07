import serial
import time

arduino_port = '/dev/ttyUSB0' #serial port for the arduino board
arduino = serial.Serial(arduino_port, 115200, timeout=.1) #open serial port
time.sleep(2) #give the serial port time to settle
arduino.write(bytes("o", 'ASCII')) #make sure both leds are off

#turn on led
arduino.write(bytes('v', 'ASCII'))
time.sleep(8)
arduino.write(bytes('v', 'ASCII'))
arduino.write(bytes('h', 'ASCII'))
time.sleep(8)
arduino.write(bytes('h', 'ASCII'))
	
arduino.close()
