#!/usr/bin/env python3
# import python libraries
import time
import getopt, sys

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy
import rcpy.mpu9250 as mpu9250

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

# no magnetometer
# mpu9250.initialize(enable_magnetometer = True)
mpu9250.initialize()

# keep running
while True:

    # running
    if rcpy.get_state() == rcpy.RUNNING:

        # temp = mpu9250.read_imu_temp()
        data = mpu9250.read()

        print("Accel,\tX:{} m/s^2\t Y:{} m/s^2\t Z:{} m/s^2\t\tGyro, X:{} deg/s\t Y:{} deg/s\t Z:{} deg/s".format(round(data['accel'][0],3) , round(data['accel'][1],3) , round(data['accel'][2],3) , round(data['gyro'][0],3) , round(data['gyro'][1],3) , round(data['gyro'][2],3) ))

    # sleep some
    time.sleep(.5)
