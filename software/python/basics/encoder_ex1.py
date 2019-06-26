#This example reads left and right encoders and outputs the position (deg) to the terminal
# Left has address 40 and right has 41
# Code for Beagle Hardware

import Adafruit_GPIO.I2C as Adafruit_I2C
import time
import numpy as np


encL = Adafruit_I2C.Device(0x40,1) # encoder i2c address
encR  = Adafruit_I2C.Device(0x41,1) # encoder i2c address

def read():
    try:
        x = encL.readU16(0xFE)
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle0 = meas*0.0219
    except:
        print('Warning (I2C): Could not read encoder0')
        angle0 = 0
    try:
        x = encR.readU16(0xFE)
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle1 = meas*0.0219 # convert to degrees
    except:
        print('Warning (I2C): Could not read encoder1')
        angle1 = 0
    angles = np.array([angle0,angle1])
    return angles



# UNCOMMENT THIS SECTION TO USE ENCODER_EX2.PY AS A STANDALONE PROGRAM
# ------------------------------------------------------------------------------
# while 1:
#     encValues = read()
#     # round the values and print them separated by a tab
#     print("Left: ",round(encValues[0],1),"\t","Right: ",round(encValues[1],1))

#     time.sleep(0.1)
