# This program takes the encoder values from encoders, computes wheel movement
# and computes the movement of the wheelbase center based on SCUTTLE kinematics.

import encoder_ex1 as enc # local library for encoders
import numpy as np			 # library for math operations
import time					 # library for time access

#define kinematics
R = 0.041 # radius in meters
L = 0.201 # half of wheelbase meters
gap = 130 # degress specified as limit for rollover

A = np.array([[-R/2*L, R/2*L],[R/2, R/2]])
wait = 0.05 #in seconds so it would be 40 ms


# global info on movements
#latest_speeds = np.zeros(2, )

def grab_travel(degL0,degL1): # calculate the delta on Left wheel
    travL = 0
    if(abs(abs(degL1) - abs(degL0)) < 1 ):
    	travL = 0 #ignore tiny movements
    elif(abs(abs(degL1) - abs(degL0)) < gap ): # if movement is small (no rollover)
    	if(degL1 > degL0 + 2): travL = (degL1 - degL0) # if movement is positive
    	elif(degL0 > degL1 + 2): travL = (degL1 - degL0) # if movement is negative
    elif(degL0 - degL1 > gap):
    	travL = ((degL1 + 360.0) - degL0) # if movement is large (rollover)
    elif(degL1 - degL0 > gap):
    	travL = (degL1 - (degL0 + 360.0)) # reverse and large (rollover)
    return(travL)

def getPhiDots():
    global latest_speeds
    encoders = enc.readEncs()       # grabs the current encoder readings in degrees

    degL0 = round(encoders[0],1)    # reading in degrees.
    degR0 = round(encoders[1],1)    # reading in degrees.
    t1 = time.time()                # time.time() reports in seconds
    time.sleep(wait)              # delay specified amount
    encoders = enc.readEncs()       # grabs the current encoder readings in degrees
    degL1 = round(encoders[0],1)    # reading in degrees.
    degR1 = round(encoders[1],1)    # reading in degrees.
    t2 = time.time()                # reading about .003 seconds
    deltaT = round((t2 - t1),3)

    #---- movement calculations
    travL = grab_travel(degL0,degL1) #grabs travel of left wheel in radians
    travL = -1 * travL # this wheel is inverted from the right side
    degL0 = degL1 # setup for next loop
    travR = grab_travel(degR0,degR1) #grabs travel of right wheel in radians
    degR0 = degR1 # setup for next loop

    # build an array of wheel speeds in rad/s
    travs = np.array([travL, travR])
    travs = travs * 0.5 # pulley ratio = 0.5 wheel turns per pulley turn
    travs = travs * np.pi / 180 # convert degrees to radians
    travs = np.round(travs,decimals=3) # round the array
    #print("travels:", travs)
    speeds = travs / deltaT
    speeds = np.round(speeds, decimals=3)
    latest_speeds = speeds #store the updated most recent speeds to the class variable
    #return(speeds)

def getMotion():
    B = getPhiDots()             # store phidots to array B (here still in rad/s)
    C = np.matmul(A,B)          # perform matrix multiplication
    C = np.round(C,decimals=3)  # round the matrix
    return(C) # returns a matrix containing thetaDot & xDot

# UNCOMMENT THIS SECTION TO RUN AS A STANDALONE PROGRAM
# while 1:
#     C = getMotion()
#     print("thetadot,xdot", C)
