# Example to read left and right encoders.
# Left has address 40 and right has 41
# Code for Pi setup.

import smbus
import time

bus=smbus.SMBus(1)

left_encoder  = 0x40 # encoder i2c address
right_encoder = 0x41 # encoder i2c address

def read_encoders_angle(encL,encR):
    try:
        x = bus.read_byte_data(encL,0xFE)
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle0 = meas*0.0219 # convert to degrees
    except:
        print('Warning (I2C): Could not read left encoder')
        angle0 = 0
    try:
        x = bus.read_byte_data(encR,0xFE)
        print
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle1 = meas*0.0219 # convert to degrees
    except:
        print('Warning (I2C): Could not read right encoder')
        angle1 = 0
    return [angle0, angle1]


while 1:
    x = read_encoders_angle(left_encoder, right_encoder)
    print("Left: ",round(x[0],3),"\t","Right: ",round(x[1],3))
    time.sleep(0.1)
