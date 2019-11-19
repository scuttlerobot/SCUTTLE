# Level 3 program for driving SCUTTLE using a GamePad

# IMPORT EXTERNAL LIBRARIES
import time
import numpy as np # for handling matrices

# IMPORT INTERNAL PROGRAMS
import L2_speed_control as sc # closed loop control. Import speed_control for open-loop
import L2_inverse_kinematics as inv #calculates wheel parameters from chassis
import L2_kinematics as kin    # calculates chassis parameters from wheels
import L2_log as log # log live data to local files

# Initialize variables for control system
t0 = 0  # time 0
t1 = 1 # time 1
e00 = 0 # previous previous error
e0 = 0 # previous error
e1 = 0 # error
dt = 0 # delta-time
de_dt = np.zeros(2) # initialize the de_dt
count = 0

while(1):
    # THIS CODE IS FOR CLOSED LOOP control
    pdTargets = inv.getPdTargets() # populates target phi dots from GamePad
    pdTargets = np.array([1, -1]) # override the gp data
    print("targets:", pdTargets)
    kin.getPdCurrent() # capture latest phi dots & update global variable
    pdCurrents = kin.pdCurrents # assign the global variable value to a local var
   
    # THIS BLOCK UPDATES VARS FOR CONTROL SYSTEM
    t0 = t1  # assign time0
    t1 = time.time() # capture current time
    dt = t1 - t0 # calculate delta-t
    e00 = e0 # assign previous previous error
    e0 = e1  # assign previous error
    e1 = pdCurrents - pdTargets # calculate the latest error
    de_dt = (e1 - e0) / dt # calculate derivative of error
    
    # CALLS THE CONTROL SYSTEM TO ACTION
    sc.driveClosedLoop(pdTargets, pdCurrents, de_dt)  # call the control system
    time.sleep(0.05)
    
    # u = sc.u 
    # u_proportional = sc.u_proportional
    # u_integral = sc.u_integral
    # u_derivative = sc.u_derivative
