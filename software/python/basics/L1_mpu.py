# This program accesses info from the Blue's onboard sensor, MPU9250
# It reads accelerometer, gyro, and magnetometer data from the sensor.

#!/usr/bin/env python3
import time # for time.sleep function
import getopt, sys
import numpy as np

import rcpy # import rcpy library (this automatically initializes robotics cape)
import rcpy.mpu9250 as mpu9250


rcpy.set_state(rcpy.RUNNING) # set state to rcpy.RUNNING
mpu9250.initialize(enable_magnetometer = True) # by default, mag is not initialized. Uncomment for mag usage.
mpu9250.initialize() # initialize the sensor

def getAccel():
    data = mpu9250.read() # this command returns a string with many parameters.
    a1 = round(data['accel'][0],3)
    a2 = round(data['accel'][1],3)
    a3 = round(data['accel'][2],3)
    axes = np.array([a1, a2, a3])
    return(axes)
    
def getAll():
    data = mpu9250.read() # this command returns a string with many parameters.
    return(data)
    
def getTemp():
    temp = mpu9250.read_imu_temp() # this command returns just temperature

# UNCOMMENT THE SECTION BELOW TO RUN AS A STANDALONE PROGRAM
# while True:
#     if rcpy.get_state() == rcpy.RUNNING: # verify the rcpy package is running
#         data = getAll()
#         print("Accel,\tX:{} m/s^2\t Y:{} m/s^2\t Z:{} m/s^2\t\tGyro, X:{} deg/s\t Y:{} deg/s\t Z:{} deg/s" \
#         .format(round(data['accel'][0],3) , round(data['accel'][1],3) , round(data['accel'][2],3) , round(data['gyro'][0],3) , \
#         round(data['gyro'][1],3) , round(data['gyro'][2],3) ))

#     time.sleep(.5) # delay 0.5s