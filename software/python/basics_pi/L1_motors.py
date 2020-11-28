# Motors Program for SCUTTLE running RasPi
# This example sends commands to two motors on the appropriate pins for H-bridge
# For pin mapping, see Wiring Guide Pi on the SCUTTLE webpage.
# Last update: 2020.11

# Import external libraries
import gpiozero                         # used for PWM outputs
from gpiozero import PWMOutputDevice
import time

# Info on pins:
# Broadcom (BCM) pin numbering for Pi gives names of GPIO17
# and GPIO18 to physical pins 11 and 12
leftOutA = gpio.PWMOutputDevice(17, frequency=1000,initial_value=0)
leftOutB = gpio.PWMOutputDevice(18, frequency=1000,initial_value=0)

RightOutA = gpio.PWMOutputDevice(22, frequency=1000,initial_value=0)
RightOutB = gpio.PWMOutputDevice(23, frequency=1000,initial_value=0)

# Channel refers to left(0) or right(1)
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

# THIS LOOP ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    while(1):
        print("motors.py: driving fwd")
        MotorL(0.6)                         # gentle speed for testing program. 0.3 PWM may not spin the wheels.
        MotorR(0.6)
        time.sleep(4)                       # run fwd for 4 seconds
        print("motors.py: driving reverse")
        MotorL(-0.6)
        MotorR(-0.6)
        time.sleep(4)                       # run reverse for 4 seconds