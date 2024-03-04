#!/usr/bin/env python3
import serial
import time

if __name__=='__main__':
	ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
	ser.reset_input_buffer()

	while True:
		data_to_send = "H"
		ser.write(data_to_send.encode())
		time.sleep(1)
