#!/usr/bin/python


#import chirp_modbus
import minimalmodbus
import time
import numpy as np
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

minimalmodbus.BAUDRATE = 9600
ADDRESS = 1
rs1 = 13
rs2 = 5
rs3 = 6

clickCounter = 0

GPIO.setup(rs1, GPIO.IN,  pull_up_down=GPIO.PUD_UP)    
GPIO.setup(rs2, GPIO.IN,  pull_up_down=GPIO.PUD_UP)    
GPIO.setup(rs3, GPIO.IN,  pull_up_down=GPIO.PUD_UP)    

def first_switch(channel):
    global clickCounter
    clickCounter+=1
    print(clickCounter)  

def second_switch(channel):
    global clickCounter
    clickCounter+=1
    print(clickCounter)    

def third_switch(channel):
    global clickCounter
    clickCounter+=1
    print(clickCounter)    

GPIO.add_event_detect(rs1, GPIO.FALLING, callback=first_switch, bouncetime=300)  
GPIO.add_event_detect(rs2, GPIO.FALLING, callback=second_switch, bouncetime=300)  
GPIO.add_event_detect(rs3, GPIO.FALLING, callback=third_switch, bouncetime=300)  

#minimalmodbus.TIMEOUT=0.5
#minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True


#MODBUS setup
motor = minimalmodbus.Instrument('/dev/ttyUSB0', slaveaddress=ADDRESS)
maxSpeed = 5*60
accTime = 4*100

motor.write_register(3, accTime, functioncode=6) #akseleravimo laikas, s*100
motor.write_register(4, maxSpeed, functioncode=6, signed=True) #greitis

#motor.precalculate_read_size=False
motor.debug=True
    

#while True:
def main():
    print("start")
    #motor.write_register(0, 0b0000000000000100, functioncode=6)
    startTime = time.time()
    #print(startTime)
    motor.write_register(0, 0b0000000000000101, functioncode=6) #start
    #start (101 fault reset, run)
    while True:
        #if (clickCounter == 100):
         #   print("stop")
        s = time.time() - startTime
        print(s)
        print(clickCounter)
        if s > 5:
            print(clickCounter)
            #motor.write_register(3, accTime, functioncode=6) #akseleravimo laikas, s*100
            motor.write_register(0, 0b0000000000000110, functioncode=6)#stop#stop
            print(clickCounter)
            
            break
    GPIO.cleanup() # this ensures a clean exit  
    #sleep(100)
    #rotate(fwd)
    #readSwitch(rs3)
    #sleep(sleepValue)
    #rotate(-1*fwd)
    #print("finished")
    #motor.write_register(0, 0b0000000000000001, functioncode=6)#stop



if __name__ == "__main__":
      main()
     