# Lab8Template.py
# Team Number:
# Hardware TM:
# Software TM:
# Date:
# Code purpose: Collect measurements from the SICK TiM561 LIDAR device
# perform a simple analysis to find the nearest obstacle, and return the angle
# and distance into two log files for passing to NodeRed.

# Import external libraries
import numpy as np  # for handling numpy arrays
import time # for timekeeping

# Import internal programs
import L2_vector as vector
import L2_log as log

tRefresh = 0.120 # target refresh time for the loop (sec)

# Start the program
print("Running Lab8Template.py")
while(1):
    t0 = time.time() # sample present time
    p2 = vector.getNearest() # store the nearest obstacle as point 2 [meters, degrees]
    log.tmpFile(p2[0], "p2_distance.txt")  # log the distance for nodeRed pickup
    log.tmpFile(np.round(p2[1],1), "p2_offset.txt") # log the angle for nodeRed pickup
    t1 = time.time() # sample present time
    tSweep = t1-t0 # output sec
    if tSweep <= tRefresh: # add a delay if the sweep was less than desired refresh speed
        time.sleep( tRefresh - tSweep) # Run your loop faster than the NodeRed sampling but slower than 15hz
    tSweep = round(tSweep*1000,0) # output ms
    t2 = time.time() # sample current time
    tLoop = round(1000*(t2-t0),0) # output ms
    print("SweepTime (ms):", tSweep,"\t","loopTime (ms):",tLoop) # print the execution times.
