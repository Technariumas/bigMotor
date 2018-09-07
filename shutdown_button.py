#!/usr/bin/python
# -*- coding: utf-8 -*-
# example gpiozero code that could be used to have a reboot
#  and a shutdown function on one GPIO button
# scruss - 2017-10
import minimalmodbus
minimalmodbus.BAUDRATE = 9600
ADDRESS = 1
#MODBUS setup
motor = minimalmodbus.Instrument('/dev/serial/by-id/usb-1a86_5523-if00-port0', slaveaddress=ADDRESS)
motor.debug=True

use_button=27                       # lowest button on PiTFT+

from gpiozero import Button
from signal import pause
from subprocess import check_call
import os

held_for=0.0

def rls():
	global held_for
	if (held_for > 5.0):
		#check_call(['/sbin/poweroff'])
		print('shutdown')
		held_for = 0.0
		motor.write_register(0, 0b0000000000000110, functioncode=6)#stop#stop
                check_call(['/sbin/poweroff'])

	elif (held_for > 2.0):
		print('stop motor')
		#check_call(['/sbin/reboot'])
		motor.write_register(0, 0b0000000000000110, functioncode=6)#stop#stop
		os.system("sudo systemctl stop motor.service")
		print('motor service killed')
                held_for = 0.0
	else:
		held_for = 0.0
def hld():
	global held_for
	# callback for when button is held
	#  is called every hold_time seconds global held_for
	# need to use max() as held_time resets to zero on last callback
	held_for = max(held_for, button.held_time + button.hold_time)

button=Button(use_button, hold_time=1.0, hold_repeat=True)
button.when_held = hld
button.when_released = rls

pause() # wait forever
