# Lab6Template.py
# Team Number:
# Hardware TM:
# Software TM:
# Date:
# Code purpose: A Program for demonstrating PID feedback control for SCUTTLE wheelspeed.
# This program is to be used to begin Lab 6 exercises (covering PID control).

# IMPORT EXTERNAL ITEMS
import time
import numpy as np # for handling matrices
import threading # only used for threading functions
import math
import csv

# IMPORT INTERNAL ITEMS
import L2_speed_control as sc # closed loop control. Import speed_control for open-loop
import L2_inverse_kinematics as inv #calculates wheel parameters from chassis
import L2_kinematics as kin    # calculates chassis parameters from wheels
import L2_log as log # log live data to local files
#import L1_gamepad as gp # for accessing gamepad directly

# CREATE A FUNCTION FOR DRIVING
def loop_drive():
    count = 0 # number of loop iterations
    # INITIALIZE VARIABLES FOR CONTROL SYSTEM
    t0 = 0  # time sample
    t1 = 1  # time sample
    e00 = 0 # error sample
    e0 = 0  # error sample
    e1 = 0  # error sample
    dt = 0  # delta in time
    de_dt = np.zeros(2) # initialize the de_dt
    
    while(1):
        count += 1 #count the number of times this loop has run
        # THIS CODE IS FOR OPEN AND CLOSED LOOP control
        pdTargets = np.array([9.7, 9.7]) # Input requested PhiDots (radians/s)
        #pdTargets = inv.getPdTargets() # populates target phi dots from GamePad
        kin.getPdCurrent() # capture latest phi dots & update global var
        pdCurrents = kin.pdCurrents # assign the global variable value to a local var
        
        # THIS BLOCK UPDATES VARIABLES FOR THE DERIVATIVE CONTROL
        t0 = t1  # assign t0
        t1 = time.time() # generate current time
        dt = t1 - t0 # calculate dt
        e00 = e0 # assign previous previous error
        e0 = e1  # assign previous error
        e1 = pdCurrents - pdTargets # calculate the latest error
        de_dt = (e1 - e0) / dt # calculate derivative of error
        
        # CALLS THE CONTROL SYSTEM TO ACTION
        #sc.driveOpenLoop(pdTargets)  # call on open loop
        sc.driveClosedLoop(pdTargets, pdCurrents, de_dt)  # call on closed loop
        time.sleep(0.05) # this time controls the frequency of the controller
        
        # u = sc.u # calculate the control effort
        # u_proportional = sc.u_proportional
        # u_integral = sc.u_integral
        # u_derivative = sc.u_derivative
        
        # THIS BLOCK OUTPUTS DATA TO A CSV FILE
        if count == 1:  # check if this is the first iteration of the loop
            log.clear_file() # clear old contents from the csv file
            log.csv_write([count,pdCurrents[0], pdTargets[0]]) # log this iteration
        elif count > 1 and count <= 400:  # only log 400 samples and then quit logging
            log.csv_write([count,pdCurrents[0],pdTargets[0]]) # log this iteration
            
loop_drive() # call the function
