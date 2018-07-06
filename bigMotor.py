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
    print("1")
    global clickCounter
    clickCounter+=1

def second_switch(channel):
    print("2")
    global clickCounter
    clickCounter+=1

def third_switch(channel):
    print("3")
    global clickCounter
    clickCounter+=1

GPIO.add_event_detect(rs1, GPIO.FALLING, callback=first_switch, bouncetime=150)  
GPIO.add_event_detect(rs2, GPIO.FALLING, callback=second_switch, bouncetime=150)  
GPIO.add_event_detect(rs3, GPIO.FALLING, callback=third_switch, bouncetime=150)  

#minimalmodbus.TIMEOUT=0.5
#minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True


#MODBUS setup
motor = minimalmodbus.Instrument('/dev/ttyUSB0', slaveaddress=ADDRESS)


#motor.precalculate_read_size=False
motor.debug=False

def setSpeed(hz):
    maxSpeed = hz*60
    motor.write_register(4, maxSpeed, functioncode=6, signed=True) #greitis
    

def start():
    motor.write_register(0, 0b0000000000000101, functioncode=6) #start

def stop():
    motor.write_register(0, 0b0000000000000110, functioncode=6)#stop#stop

def setAcc(s):
    accTime = s*100
    motor.write_register(3, accTime, functioncode=6) #akseleravimo laikas, s*100

def down(clickLimit):
    global clickCounter
    clickCounter = 0
    start()
    print("start")
    while True:
        #print(clickCounter)
        if (clickCounter > clickLimit):
               print(clickCounter)
               stop()
               time.sleep(1)
               break


def rotate(clickLimit):
    global clickCounter
    clickCounter = 0
    start()
    print("start")
    while True:
        print(clickCounter)
        if (clickCounter > clickLimit):
               print(clickCounter)
               stop()
               time.sleep(1)
               break
    

def main():
    speed = -5
    setAcc(0.5) #seconds
    clickLimit = 30
    #while True:
    dir = 1
    #setSpeed(dir*speed) #Hz
    #setSpeed(speed) #Hz

    #down(clickLimit)
    for i in range(0, 1):
            setSpeed(speed) #Hz
            print("fwd", clickCounter)
            rotate(clickLimit)
            setSpeed(-speed) #Hz
            print("back", clickCounter)
            rotate(clickLimit)  
              
    GPIO.cleanup() # this ensures a clean exit  

if __name__ == "__main__":
      main()
     