# Lab8Template.py
# Team Number:
# Hardware TM:
# Software TM:
# Date:
# Code purpose: Collect measurements from the SICK TiM561 LIDAR device
# perform a simple analysis to find the nearest obstacle, and return the angle
# and distance into two log files for passing to NodeRed

# Import external libraries
import numpy as np
import time

# Import internal programs
import L2_Lidar.py as lidar
import L2_log as log

while(1):
    scan = lidar.scan()
    time.sleep(0.005) # very small delay.
