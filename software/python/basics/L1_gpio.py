# This code writes and reads from the GPIO pins available on the BeagleBone Blue
# BeagleBone Blue Pinout https://github.com/beagleboard/beaglebone-blue/wiki/Pinouts
# Uses Adafruit library
# Created by Team NexTec

# Import external librarires
import Adafruit_BBIO
from Adafruit_BBIO.GPIO import *
import time

# These GPIO variable pin names can be referenced in the BeagleBone Blue Pinout diagram (link in description above)
#LEDs
USR_LED0 = "USR0"
USR_LED1 = "USR1"
USR_LED2 = "USR2"
USR_LED3 = "USR3"
LED_RED = "RED_LED"
LED_GREEN = "GREEN_LED"
#OUTPUTS
GPIO1_25 = "GP0_3"
GPIO1_17 = "GP0_4"
GPIO3_20 = "GP0_5"
GPIO3_17 = "GP0_6"
GPIO3_2 = "GP1_3"
GPIO3_1 = "GP1_4"
#INPUTS
GPIO1_17 = "GP0_4"
GPIO3_17 = "GP0_6"

#MODES
OUTPUT = 1
INPUT = 0

#STATES
HIGH = 1
LOW = 0

# Initialize GPIO pin as either Output or Input
def init(Pin, Mode):
    setup(Pin, Mode)

# Write to Output GPIO pin as either High or Low
def write(Pin, State):
    output(Pin, State)

# Read State (High or Low) of Input GPIO pin 
def read(Pin):
    State = input(Pin)
    return(State)

# # UNCOMMENT THE SECTION BELOW TO RUN AS STANDALONE CODE
# init(USR_LED0, OUTPUT)
# while 1:
#     print("LED ON")
#     write(USR_LED0, HIGH)
#     time.sleep(3)
#     print("LED OFF")
#     write(USR_LED0, LOW)
#     time.sleep(2)
