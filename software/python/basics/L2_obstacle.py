# this program was designed for detecting obstacles using lidar.
# it is a level 2 program.

import time
import L1_lidar as lidar  # import the level 1 program
import numpy as np # for operating on arrays

p0 = np.asarray([0,0]) #define p0, which is the location of the lidar (x and y).
p1 = np.asarray([0.300,0.0]) # define p1, which is the location of interest for collisions (meters)
num_points = 54 # Desired number of points in your scan (54 has been tested)

def nearest_point(): # this function returns the nearest object to point p0

    scan_points = lidar.polarScan(num_points)
    # convert the polar coordinates into cartesian
    scan_cart = np.zeros((num_points,2))
    d = len(scan_cart) # return the number of elements in scan
    for d in range(d):
        scan_cart[d,0]=scan_points[d,0]*np.cos(np.radians(scan_points[d,1]))
        scan_cart[d,1]=scan_points[d,0]*np.sin(np.radians(scan_points[d,1]))

    # calculate the distances between p0 and scan x_points
    vector_lengths = np.zeros(num_points)
    k = 0.004 # minimum distance for a reading considered to be valid
    d = len(scan_cart) #return the number of elements in scan
    for d in range(d):
        a = scan_cart[d,0]-p1[0] # difference in x values
        b = scan_cart[d,1]-p1[1] # difference in y values
        c = np.sqrt(a**2 + b**2) # take the hypotenuse
        if c < k:
            c = 5.0 # for nonvalid measurements, raise to 5 meters
        vector_lengths[d]= c # assign hypotenuse to vector length


    #"filter" returns array of all values greater than k, and min finds the minimum
    d_min = min(filter(lambda x: x > k, vector_lengths))
    myIndex = np.argmin(vector_lengths)
    myYValue =  scan_cart[myIndex,1] #column 1 is y values in scan_cart
    myPoint = np.array([ d_min, myYValue ])
    myPoint = np.round(myPoint, decimals = 3)
    #print(d_min) #print out the closest detected obstacle
    return(myPoint)

# UNCOMMENT THIS SECTION TO USE AS A STANDALONE PROGRAM
# ------------------------------------------------------------------------------

# while 1:
#     obstacle = nearest_point()
#     print(obstacle)
#     time.sleep(0.2) # TiM scan speed is 15hz.  Take 1/3 of readings.
