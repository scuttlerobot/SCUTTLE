# This File performs the following:
# 1) grab a subset of the readings from the lidar for lightweight purposes
# 2) assign the proper angle value to the reading, with respect to robot x-axis
# 3) create a 2d array of [distances, angles] from the data
# 4) find the point in the array that is closest to P1 (point of interest regarding collision)

import numpy as np # for array handling
import pysicktim as lidar # required for communication with TiM561 lidar sensor

np.set_printoptions(suppress=True)  # Suppress Scientific Notation

p0 = np.asarray([0,0]) #define p0, which is the location of the lidar (x and y).
p1 = np.asarray([0.300,0.0]) # define p1, which is the location of interest for collisions (meters)

start_angle = -135.0 # lidar points will range from -135 to 135 degrees
num_points = 54 # Desired number of points

def nearest_point():

    lidar.scan() #take reading

    # LIDAR data properties
    dist_amnt = lidar.scan.dist_data_amnt   # Number of distance data points reported from the lidar
    angle_res = lidar.scan.dist_angle_res   # Angular resolution reported from lidar

    # create the column of distances
    scan_points = np.asarray(lidar.scan.distances) #store the reported readings and cast as numpy.array
    inc_ang = (dist_amnt/(num_points+1))*angle_res  # Calculate angle increment for scan_points resized to num_points
    scan_points = np.asarray(np.array_split(scan_points,num_points))  # Split array into sections
    scan_points = [item[0] for item in scan_points]   # output first element in each section into a list
    scan_points = np.asarray(scan_points) # cast the list into an array
    scan_points = np.reshape(scan_points,(scan_points.shape[0],1)) # Turn scan_points row into column

    #create the column of angles
    angles = np.zeros(54)
    x = len(angles)
    for i in range(x): #run this loop
        angles[i] = (i*lidar.scan.dist_angle_res*lidar.scan.dist_data_amnt/num_points)+(start_angle)
    angles = np.reshape(angles,(angles.shape[0],1))  # Turn angles row into column

    #create the polar coordinates of scan
    scan_points = np.hstack((scan_points,angles))    # Turn two (54,) arrays into a single (54,2) matrix
    scan_points = np.round(scan_points,3) # Round each element in array to 3 decimal places

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

# Current output is a (54,2) matrix
# [distance(scan_points), theta(degrees)]

# print(scan_points[:,1])
# print(degrees)
