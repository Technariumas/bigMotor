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
    #print("1", clickCounter)

def second_switch(channel):
    global clickCounter
    clickCounter+=1
    #print("2", clickCounter)

def third_switch(channel):
    global clickCounter
    clickCounter+=1
    #print("3", clickCounter)

bouncetime = 100

GPIO.add_event_detect(rs1, GPIO.RISING, callback=first_switch, bouncetime=bouncetime)  
GPIO.add_event_detect(rs2, GPIO.RISING, callback=second_switch, bouncetime=bouncetime)  
GPIO.add_event_detect(rs3, GPIO.RISING, callback=third_switch, bouncetime=bouncetime)  

#minimalmodbus.TIMEOUT=0.5
#minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True


#MODBUS setup
motor = minimalmodbus.Instrument('/dev/serial/by-id/usb-1a86_5523-if00-port0', slaveaddress=ADDRESS)


#motor.precalculate_read_size=False
motor.debug=True

def readSwitches():
    while True:
        time.sleep(30)

def setSpeed(hz):
    maxSpeed = hz*60
    motor.write_register(4, maxSpeed, functioncode=6, signed=True) #greitis

def heartBeat():
    ret = motor.read_register(registeraddress=4, functioncode=3)
    #print("Status: "+str(ret))

def start():
    motor.write_register(0, 0b0000000000000101, functioncode=6) #start

def stop():
    motor.write_register(0, 0b0000000000000110, functioncode=6)#stop#stop

def setAcc(s):
    accTime = s*100
    motor.write_register(3, accTime, functioncode=6) #akseleravimo laikas, s*100

def move(clickLimit, speed):
    setSpeed(speed)
    global clickCounter
    clickCounter = 0
    start()
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
    while True:
        #print(clickCounter)
        if (clickCounter > clickLimit):
               #print(clickCounter)
               stop()
               time.sleep(0.2)
               break

def cycle(clickLimit, speed, cycles):
    for i in range(cycles):
            setSpeed(speed) #Hz
            print("fwd", clickCounter)
            rotate(clickLimit)
            setSpeed(-speed) #Hz
            print("back", clickCounter)
            rotate(clickLimit) 

def lift(duration, speed):
    setSpeed(speed)
    start()
    time.sleep(duration)
    stop()

def rawCycle(duration, speed, cycles):
    for i in range(cycles):
            n = duration     
            setSpeed(speed) #Hz
            #print("fwd", clickCounter)
            #rotate(clickLimit)
            start()
            while (n > 0):
                heartBeat()
                time.sleep(1)
                n-=1
                print(n)
            stop()
            n = duration
            #time.sleep(0.02)
            setSpeed(-speed) #Hz
            start()
            while (n > 0):
                heartBeat()
                time.sleep(1)
                print("back", n)
                n-=1
            stop()
            #time.sleep(0.02)

def main():
    UP = -1
    DOWN = 1
    direction = UP
    speed = direction*8 #8
    setAcc(5) #5
    #clickLimit = 12
    cycles = 3
    duration = 17#17
    time.sleep(1)
    #readSwitches()
    #cycle(clickLimit, speed, cycles)
    #lift(speed, 6)
    while True:
        #time.sleep(10)
        #print("Big motor is runing!")
        rawCycle(duration, speed, cycles)
    #lift(speed, 3)
    #move(clickLimit, direction*speed)
 
              
    GPIO.cleanup() # this ensures a clean exit  

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        stop()
    
     
