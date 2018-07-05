#!/usr/bin/python


#import chirp_modbus
import minimalmodbus
from time import sleep
import numpy as np
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

minimalmodbus.BAUDRATE = 9600
ADDRESS = 1
rs1 = 13
rs2 = 5
rs3 = 6

GPIO.setup(rs1, GPIO.IN,  pull_up_down=GPIO.PUD_UP)    
GPIO.setup(rs2, GPIO.IN,  pull_up_down=GPIO.PUD_UP)    
GPIO.setup(rs3, GPIO.IN,  pull_up_down=GPIO.PUD_UP)    

def first_switch(channel):  
    print "falling edge detected by rs1"  

GPIO.add_event_detect(rs1, GPIO.FALLING, callback=first_switch, bouncetime=300)  
GPIO.add_event_detect(rs2, GPIO.FALLING, callback=second_switch, bouncetime=300)  
GPIO.add_event_detect(rs3, GPIO.FALLING, callback=third_switch, bouncetime=300)  

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

def readSwitch(rs):
    while True:
        if GPIO.input(rs) == 0:
           print("switching")
           sleep(0.01)



#while True:
def main():
    sleep(100)
    #rotate(fwd)
    #readSwitch(rs3)
    #sleep(sleepValue)
    #rotate(-1*fwd)
    #print("finished")
    #motor.write_register(0, 0b0000000000000001, functioncode=6)#stop



if __name__ == "__main__":
    main()