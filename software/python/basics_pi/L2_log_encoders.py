# This program takes the encoder values from encoders,  
# and logs that data to a local file to be accessed in NodeRed.

# THIS PROGRAM IS IN PROGRESS AS OF 2021.9

# Import external libraries
import numpy as np   # library for math operations
import time   # library for time access
import smbus2   # a Python package to communicate over i2c

# Import local files
import L1_encoder as enc                
import L1_log as log                       

# Print the values in the terminal and log to file used in NodeRed
if __name__ == "__main__":
    print ("Reading Encoder Values")
    while True:
        # Set the encoder values as new variables
        rsp = enc.readShaftPositions() # read the values.  Reading will only change if motor pulley moves
        left = rsp[0]
        right = rsp[1]
        print ("Left Encoder:",left,"\t","Right Encoder:",right)   # prints the left and right encoder values in the terminal
        log.tmpFile(left, "lenc.txt")   # logs left encoder values to tmp file to be displayed in NodeRed
        log.tmpFile(right, "renc.txt")   # logs right encoder values to tmp file to be displayed in NodeRed
