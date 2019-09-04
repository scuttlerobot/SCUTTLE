# L3_telemetry.py
# This file will log data to NodeRed.
# Access nodered at 192.168.8.1:1880 (by default, it's running on the Blue)

# Import Internal Programs
import L1_mpu as mpu
import L2_log as log

# Import External programs
import numpy as np
import time

# Run the main loop    
while 1:
    accel = mpu.getAccel() # call the function from within L1_mpu.py
    (xAcc) = accel[0] # x axis is stored in the first element
    (yAcc) = accel[1] # y axis is stored in the second element
    print ("x axis:", xAcc, "y axis:", yAcc) # print the two values
    axes = np.array([xAcc, yAcc]) #store just 2 axes
    log.Node_Red2(axes)
    time.sleep(0.2)
