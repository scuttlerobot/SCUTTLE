# This example sends commands to two motors on the appropriate pins for H-bridge
# Designed for Pi hardware.

# import external libraries
import gpiozero #gpiozero is the chosen library for PWM functionality
from gpiozero import PWMOutputDevice
import time

#info on pins:
# Broadcom (BCM) pin numbering for Pi gives names of GPIO17
# and GPIO18 to physical pins 11 and 12
leftOutA = PWMOutputDevice(17, frequency=1000,initial_value=0)
leftOutB = PWMOutputDevice(18, frequency=1000,initial_value=0)

RightOutA = PWMOutputDevice(22, frequency=1000,initial_value=0)
RightOutB = PWMOutputDevice(23, frequency=1000,initial_value=0)

# This section shows another way to assign parameters if uncommented
# leftOutA.frequency = 1000 #this is redundant
# leftOutA.value = 0.0 # this is for duty cycle

#channel refers to left(0) or right(1)
def MotorL(speed):
    if speed>0:
        leftOutB.value = speed
        leftOutA.value = 0
    elif speed<0:
        leftOutB.value = 0
        leftOutA.value = (-1*speed) #drive opposite polarity with positive duty cycle
    elif speed==0:
        leftOutB.value = 0
        leftOutA.value = 0

def MotorR(speed):
    if speed>0:
        RightOutB.value = speed
        RightOutA.value = 0
    elif speed<0:
        RightOutB.value = 0
        RightOutA.value = (-1*speed) #drive opposite polarity with positive duty cycle
    elif speed==0:
        RightOutB.value = 0
        RightOutA.value = 0

if __name__ == "__main__":              # loop only executes if program is run directly (not imported)
    while(1):
        print("motors.py: driving fwd")
        MotorL(0.6)                         # gentle speed for testing program. 0.3 PWM may not spin the wheels.
        MotorR(0.6)
        time.sleep(4)                       # run fwd for 4 seconds
        print("motors.py: driving reverse")
        MotorL(-0.6)
        MotorR(-0.6)
        time.sleep(4)                       # run reverse for 4 seconds
