# Example to read left and right encoders.
# Code for Pi setup.

import smbus
import time

bus=smbus.SMBus(1)

right_encoder = 0x40
left_encoder  = 0x41

def read_encoders_angle(enc0,enc1):
    try:
        x = bus.read_byte_data(enc0,0xFE)
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle0 = meas*0.0219
    except:
        print('Warning (I2C): Could not read encoder0')
        angle0 = 0
    try:
        x = bus.read_byte_data(enc1,0xFE)
        x = ((x << 8) | (x >> 8)) & 0xFFFF
        meas = ((x & 0xFF00) >> 2) | ( x & 0x3F)
        angle1 = meas*0.0219 # convert to degrees
    except:
        print('Warning (I2C): Could not read encoder1')
        angle1 = 0
    return [angle0, angle1]


while 1:
    x = read_encoders_angle(right_encoder,left_encoder)
    print("Left: ",round(x[0],0),"\t","Right: ",round(x[1],0))
    time.sleep(0.1)
