#!/usr/bin/python3

# L3_telemetry.py
# This program grabs data from the onboard sensors and log data in files
# for NodeRed access and integrate into a custom "flow".
# Access nodered at 192.168.8.1:1880 (by default, it's running on the Blue)

# Import Internal Programs
import L1_mpu as mpu
import L2_log as log

# Import External programs
import numpy as np
import time

# Run the main loop
while True:
    accel = mpu.getAccel()                          # call the function from within L1_mpu.py
    (xAccel) = accel[0]                             # x axis is stored in the first element
    (yAccel) = accel[1]                             # y axis is stored in the second element
    print("x axis:", xAccel, "y axis:", yAccel)     # print the two values
    axes = np.array([xAccel, yAccel])               # store just 2 axes in an array
    log.NodeRed2(axes)                              # send the data to txt files for NodeRed to access.
    time.sleep(0.2)
