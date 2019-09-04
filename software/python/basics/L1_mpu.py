# This program accesses info from the Blue's onboard sensor, MPU9250
# It reads accelerometer, gyro, and magnetometer data from the sensor.

#!/usr/bin/env python3
# import python libraries
import time
import getopt, sys

# import rcpy library (this automatically initializes robotics cape)
import rcpy
import rcpy.mpu9250 as mpu9250

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

# mpu9250.initialize(enable_magnetometer = True) # by default, mag is not initialized. Uncomment for mag usage.
mpu9250.initialize()

# UNCOMMENT THE SECTION BELOW TO RUN AS A STANDALONE PROGRAM
# while True:
#     if rcpy.get_state() == rcpy.RUNNING: # verify the rcpy package is running
#         # temp = mpu9250.read_imu_temp() # this command returns just temperature
#         data = mpu9250.read() # this command returns a string with many parameters.
#         print("Accel,\tX:{} m/s^2\t Y:{} m/s^2\t Z:{} m/s^2\t\tGyro, X:{} deg/s\t Y:{} deg/s\t Z:{} deg/s".format(round(data['accel'][0],3) , round(data['accel'][1],3) , round(data['accel'][2],3) , round(data['gyro'][0],3) , round(data['gyro'][1],3) , round(data['gyro'][2],3) ))

#     # sleep some
#     time.sleep(.5) # delay
