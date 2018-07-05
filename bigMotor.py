#!/usr/bin/python


#import chirp_modbus
import minimalmodbus
from time import sleep
import numpy as np
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

minimalmodbus.BAUDRATE = 9600
ADDRESS = 1
rs_pin = 15
GPIO.setup(rs_pin, GPIO.IN)    

#minimalmodbus.TIMEOUT=0.5
#minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

amplitude = 50 #Frequency scale
stretchFactor = 1#Stretch factor of the sine function. Makes the sine smoother, but reduces amplitude. 
nPoints = 50 #number of distinct velocity points
slowEndCutoff = 5 #too low frequency at the start and end of rotation
sleepValue = 5

fwd = np.round(amplitude*np.sin((1./stretchFactor)*np.linspace(0, np.pi/2, nPoints)))
fwd = np.concatenate([fwd, fwd[::-1]])
#fwd = fwd[slowEndCutoff:-slowEndCutoff]

#rot = np.concatenate([fwd, -1*fwd])

motor = minimalmodbus.Instrument('/dev/ttyUSB0', slaveaddress=ADDRESS)
#motor.precalculate_read_size=False
motor.debug=True
import math

def rotate(rot, sleepValue=0.1):
		for x in rot:
			try:
				print("Sine: ",x)
				# ret = motor.read_registers(registeraddress=1, numberOfRegisters=1, functioncode=4)
				ret = motor.read_register(registeraddress=5, functioncode=3)
				print("Status: "+str(ret) + " writing ...")
				motor.write_register(1, int(x), functioncode=6, signed=True) #greitis
				motor.write_register(0, 0b0000000000000101, functioncode=6) #start (101 fault reset, run)
				ret = motor.read_register(registeraddress=0, functioncode=3)
				print("returned "+str(ret))
				
			except ValueError as ve:
				print(ve)
				print("Waiting...")
				sleep(1)
			except IOError as io:
				print(io)

def readSwitch():
    while True:
        if GPIO.input(rs_pin):
           print("Door is open")
           sleep(10)
           
        if GPIO.input(rs_pin) == False:
           #print("Door is closed")
           sleep(0.1)

#while True:
def main():
    #rotate(fwd)
    readSwitch()
    #sleep(sleepValue)
    #rotate(-1*fwd)
    #print("finished")
    motor.write_register(0, 0b0000000000000001, functioncode=6)#stop

if __name__ == "__main__":
    main()