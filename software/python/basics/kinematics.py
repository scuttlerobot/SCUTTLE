# This program takes the encoder values from encoders, computes wheel movement
# and computes the movement of the wheelbase center based on SCUTTLE kinematics.

import encoder_ex2 as enc # local library for encoders
import numpy as np			 # library for math operations
import time					 # library for time access

#define kinematics
R = 0.041 # radius in meters
L = 0.201 # half of wheelbase meters
A = np.array([[-R/2*L, R/2*L],[R/2, R/2]])
deltaT = 0.10

def grab_travel(degL0,degL1): # calculate the delta on Left wheel
    travL = 0
    if(abs(abs(degL1) - abs(degL0)) < 1 ):
    	travL = 0 #ignore tiny movements
    elif(abs(abs(degL1) - abs(degL0)) < 100 ): # if movement is small (no rollover)
    	if(degL1 > degL0 + 2): travL = (degL1 - degL0) # if movement is positive
    	elif(degL0 > degL1 + 2): travL = (degL1 - degL0) # if movement is negative
    elif(degL0 - degL1 > 100):
    	travL = ((degL1 + 360.0) - degL0) # if movement is large (rollover)
    elif(degL1 - degL0 > 100):
    	travL = (degL1 - (degL0 + 360.0)) # reverse and large (rollover)
    return(travL)

def getPhiDots():
    encoders = enc.read()           # grabs the current encoder readings in degrees
    degL0 = round(encoders[0],3)    # reading in degrees.
    degR0 = round(encoders[1],3)    # reading in degrees.
    time.sleep(deltaT)              # delay specified amount
    encoders = enc.read()           # grabs the current encoder readings in degrees
    degL1 = round(encoders[0],3)    # reading in degrees.
    degR1 = round(encoders[1],3)    # reading in degrees.

    #---- movement calculations
    travL = grab_travel(degL0,degL1) #grabs travel of left wheel in radians
    travL = -1 * travL # this wheel is inverted from the right side
    degL0 = degL1 # setup for next loop
    travR = grab_travel(degR0,degR1) #grabs travel of right wheel in radians
    degR0 = degR1 # setup for next loop

    # calculate speed of wheelbase center
    travs = np.array([travL, travR])
    travs = np.round(travs,decimals=3) # round the array
    #print("travels:", travs)
    speeds = travs / deltaT
    speeds = np.round(speeds, decimals=3)
    return(speeds)

def getMotion():
    B = getPhiDots()             # store phidots to array B
    C = np.matmul(A,B)          # perform matrix multiplication
    C = np.round(C,decimals=3)  # round the matrix
    return(C) # returns a matrix containing thetaDot & xDot

while 1:
    C = getMotion()
    print("thetadot,xdot", C)
