# Servo Program for SCUTTLE running RasPi
# This example sends commands to two servos (50hz standard servos)
# Great reference: https://lastminuteengineers.com/servo-motor-arduino-tutorial/

# Import external libraries
import gpiozero                             # used for PWM outputs
from gpiozero import PWMOutputDevice as pwm # for driving motors, LEDs, etc
import time                                 # for keeping time
import numpy as np                          # for handling arrays

# Import internal programs
import L1_gamepad as gp

frq = 50                                    # servo driving frequency
# Broadcom (BCM) pin numbering for RasPi is as follows: PHYSICAL:       NAME:
servo1  = pwm(12, frequency=frq,initial_value=0)        # PIN 32        GPIO12 (PWM0)
#servo2  = pwm(18, frequency=frq,initial_value=0)        # PIN 33        GPIO13 (PWM1)

def computePWM(cmd):
    in_min = -1.0   # simply -100% speed
    in_max = 1.0    # simply  100% speed
    out_min = 0.02  # 1 ms of 20 ms period is 0.05 fraction
    out_max = 0.11  # 2 ms of 20 ms period is 0.10 fraction
    in_fraction = (cmd - in_min) / (in_max - in_min)
    myPWM = in_fraction * (out_max - out_min) + out_min 
    myPWM = round(myPWM,4)
    return myPWM

def sendPWM(myPWM):     # takes a speed [-1 1] and computes proper PWM
    servo1.value = myPWM

def computePW(myPWM): # compute the actual pulse width in miliseconds
    period = 1/frq
    width = myPWM * period *1000
    width = round(width, 2)
    return width



# THIS LOOP ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY


if __name__ == "__main__":
    print("starting L2_servo.py")
    while(1):
        gp_data = gp.getGP()
        axis0 = gp_data[0] * -1
        myPWM = computePWM(axis0)
        width = computePW(myPWM)
        sendPWM(myPWM)
        print("Axis: ", axis0, "\t pwm percent: ", myPWM, " width(ms) ", width)
        time.sleep(.1)     
        
        # print("servo.py: driving forward")
        # sendPWM(0.7)
        # time.sleep(4)

        # print("PAUSING")
        # servo1.value = 0.0672 # 0.075 duty equals 1500 microseconds, to command a pause 
        # time.sleep(4)
        
        # print("servo.py: driving reverse")
        # sendPWM(-0.99)
        # time.sleep(4)

        # print("PAUSING")
        # sendPWM(0)
        # time.sleep(4)

        