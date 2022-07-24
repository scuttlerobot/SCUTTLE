# Program to read left and right encoders on SCUTTLE.
# Left has address 40 and right has 41, and the encoders are placed on
# the motor shafts, so readings indicate movement before pulley ratio
# is considered.
# This code runs on SCUTTLE with rasPi setup. (last updated 2020.11)

# Import external libraries
import smbus2       # a Python package to communicate over i2c
import numpy as np  # use numpy to build the angles array
import time         # for keeping time

bus=smbus2.SMBus(1) # declare the i2c bus object

encL = 0x40         # encoder i2c address for LEFT motor
encR = 0x41         # encoder i2c address for RIGHT motor (this encoder has A1 pin pulled high)

def singleReading(encoderSelection):                                            # return a reading for an encoder in degrees (motor shaft angle)
    try:
        twoByteReading = bus.read_i2c_block_data(encoderSelection, 0xFE, 2)     # request data from registers 0xFE & 0xFF of the encoder. Approx 700 microseconds.
        binaryPosition = (twoByteReading[0] << 6) | twoByteReading[1]           # remove unused bits 6 & 7 from byte 0xFF creating 14 bit value
        degreesPosition = binaryPosition*(360/2**14)                            # convert to degrees
        degreesAngle = round(degreesPosition,1)                                 # round to nearest 0.1 degrees
    except:
        print("Encoder reading failed.")                                        # indicate a failed reading
        degreesAngle = 0
    return degreesAngle

def readShaftPositions():                                   # read both motor shafts.  approx 0.0023 seconds.
    try:
        rawAngle = singleReading(encL)                      # capture left motor shaft
        angle0 = 360.0 - rawAngle                           # invert the reading for left side only
        angle0 = round(angle0,1)                            # repeat rounding due to math effects
    except:
        print('Warning(I2C): Could not read left encoder')  # indicate which reading failed
        angle0 = 0
    try:
        angle1 = singleReading(encR)                        # capture right motor shaft
    except:
        print('Warning(I2C): Could not read right encoder') # indicate which reading failed
        angle1 = 0
    angles = np.array([angle0,angle1])
    return angles

# THIS LOOP RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    print("Testing Encoders")
    while True:
     encValues = readShaftPositions() # read the values.  Reading will only change if motor pulley moves
     # round the values and print them separated by a tab
     print("Left: ", encValues[0], "\t","Right: ", encValues[1])
     time.sleep(0.5)
