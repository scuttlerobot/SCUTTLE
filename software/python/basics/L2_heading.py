# This program takes the magnetometer values from the compass program
# and computes a heading. The heading describes the y-vector of the robot
# minus the magnetic North vector.
# Using this program requires calibration of xRange and yRange

import L1_mpu as mpu # retrieve magnetometer info
import numpy as np        # library for math operations
import time               # library for time access

xRange = np.array([-80, 5]) # range must be updated for your device
yRange = np.array([-29, 26]) # range must be updated for your device

def getXY(): # this function returns an average of several magnetometer readings for x and y
    data = np.take(mpu.getMag(), [0,1])  # take only the first two elements of the returned array
    for i in range(10): # iterate 10 times (i will start at zero)
        newData =  np.take(mpu.getMag(), [0,1]) # call getMag and take the first two elements
        data = np.vstack((data,newData)) # vertically stack the new data array at bottom of existing data
        time.sleep(0.002) # delay 5 ms
    data_av = np.average(data, axis=0)  # take an average of the x's and y's to form new array
    data_av = np.round(data_av,3) # round the data
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
    
def getHeading(myAxes): # convert scaled values to a heading
    h = np.arctan2(myAxes[0],myAxes[1]) # atan2 uses all four quadrants to return [-180, 180] range
    return(h)
    
# # UNCOMMENT THIS SECTION TO RUN AS A STANDALONE PROGRAM
# while 1:
#     axes = getXY() # call xy function
#     print("raw values:", axes)
#     axesScaled = scale(axes) # perform scale function
#     print("scaled values:", axesScaled) # print it out
#     h = getHeading(axesScaled) # compute the heading
#     headingDegrees = round(h*180/np.pi,2)
#     print("heading:", headingDegrees)
#     time.sleep(0.25) # delay 0.25sec
