# This program takes the magnetometer values from the compass program
# and computes a heading. The heading describes the x-axis of the robot
# with respect to Magnetic North.
# Using this program requires calibration of xRange and yRange

import L1_mpu as mpu # retrieve magnetometer info
import numpy as np        # library for math operations
import time               # library for time access

xRange = np.array([-30, 40])
yRange = np.array([-32, 33])

def getXY():
    data = np.take(mpu.getMag(), [0,1])  # take only the first two elements of the returned array
    for i in range(10): # iterate 10 times (i will start at zero)
        newData =  np.take(mpu.getMag(), [0,1]) # call getMag and take the first two elements
        data = np.vstack((data,newData))
        time.sleep(0.002) # delay 5 ms
    data_av = np.average(data, axis=0)  # take an average of the x's and y's to form new array
    return(data_av)
    
def scale(axes): # convert raw values to range of [-1 1]
    # re-scale the returned values to a ratio of the value to it's maximum value (0 to 1)
    xScaled = (axes[0] - xRange[0]) / (xRange[1]-xRange[0])
    yScaled = (axes[1] - yRange[0]) / (yRange[1]-yRange[0])
    # re-center the values about zero, and expand the range to +/- 1
    xCentered = (xScaled - 0.5) * 2
    yCentered = (yScaled - 0.5) * 2
    axes = np.array([xCentered, yCentered])
    axes = np.round(axes,2)
    return(axes) # returns scaled, centered axes in range [-1 1]

# # UNCOMMENT THIS SECTION TO RUN AS A STANDALONE PROGRAM
# while 1:
#     axes = getXY() # call xy function
#     axesScaled = scale(axes) # perform scale function
#     axesScaled = np.round(axesScaled,2) # round the results to 2 decimals
#     print("scaled values:", axesScaled) # print it out
#     time.sleep(0.25) # delay 0.25sec
#     head = np.arctan(axesScaled[0]/axesScaled[1])
#     print("heading:", round(head*180/np.pi,2))
