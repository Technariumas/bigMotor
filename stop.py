#!/usr/bin/python

import minimalmodbus
minimalmodbus.BAUDRATE = 9600
ADDRESS = 1
#MODBUS setup
motor = minimalmodbus.Instrument('/dev/ttyUSB0', slaveaddress=ADDRESS)


#motor.precalculate_read_size=False
motor.debug=True
motor.write_register(0, 0b0000000000000110, functioncode=6)#stop#stop

