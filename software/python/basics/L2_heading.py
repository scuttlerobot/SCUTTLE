# This program takes the magnetometer values from the compass program
# and computes a heading. The heading describes the x-axis of the robot
# with respect to Magnetic North.

import L1_mpu as mpu # retrieve magnetometer info
import numpy as np        # library for math operations
import time               # library for time access

xRange = np.array([-6.8, 29.0])
yRange = np.array([9.7, 45.5])

def calibrateHeading():
    print("running calibration")

def getHeading():
    axes = mpu.getMag()      # store axes to an array
    return(axes)
    
def scale(xRange,yRange,x,y):
    xScaled = (x - np.average(xRange))/(xRange[1]-xRange[0])
    yScaled = (y - np.average(yRange))/(yRange[1]-yRange[0])
    axes = np.array([xScaled, yScaled])
    return(axes)                   # returns a matrix containing thetaDot & xDot

# UNCOMMENT THIS SECTION TO RUN AS A STANDALONE PROGRAM
while 1:
    axes = getHeading()
    print("unscaled:", axes)
    axesScaled = scale(xRange,yRange, axes[0], axes[1])
    axesScaled = np.round(axesScaled,2)
    print("scaled:", axesScaled)
    time.sleep(1)
    head = np.arctan(axesScaled[0]/axesScaled[1])
    print("heading:", round(head*180/np.pi,2))
    #C = getHeading()
    #print("heading (deg):", h)
