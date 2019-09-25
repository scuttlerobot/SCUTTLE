#This example reads left and right encoders and outputs the position (deg) to the terminal
# Left has address 40 and right has 41
# Code for Beagle Hardware

import Adafruit_GPIO.I2C as Adafruit_I2C
import time
import numpy as np

encL = Adafruit_I2C.Device(0x40,1) # encoder i2c address
encR  = Adafruit_I2C.Device(0x41,1) # encoder i2c address
def readEncs(channel):
    try:
        # The AS5048B encoder gives a 14 bit angular reading
        if channel == 'L':
            x = encL.readU16(0xFE) # capture the 8 msb's from encoder
            y = encL.readU16(0xFF) # capture the 6 lsb's from encoder
        elif channel == "R":
            x = encR.readU16(0xFE) # capture the 8 msb's from encoder
            y = encR.readU16(0xFF) # capture the 6 lsb's from encoder
        # y can contribute  at most 1.4 degrees to the reading
        # for x, perform bitwise operation to get true scaling of these bits
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        x = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle_raw = x   # multiplying by 0.0219 will give degrees
    except:
        print('Warning (I2C): Could not read encoder' + channel)
        angle_raw = 0  # set to zero, avoid sending wrong value
    return angle_raw   # the returned value must be scaled by 359deg / 2^14

# the READ function returns the encoder values.  Call this fcn from other programs.
def read():
    encLeft = readEncs('L')
    encRight = readEncs('R')
    encoders = np.array([encLeft,encRight])
    return encoders

# UNCOMMENT THIS SECTION TO USE ENCODER_EX2.PY AS A STANDALONE PROGRAM
# ------------------------------------------------------------------------------
# while 1:
#       encoders = read()
#       encoders = 0.0219 * encoders
#       # round the values and print them
#       print("encoders: ", encoders)
#       time.sleep(0.1)
