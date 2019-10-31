# Lab7Template.py
# Team Number:
# Hardware TM:
# Software TM:
# Date:
# Code purpose: DRIVING BY COLOR TRACKING WITH CLOSED-LOOP STEERING CONTROL
#   This program captures an image, discovers a target within your HSV range
#   Generates a pixel location of the target, and estimates the angle of the
#   target from the camera's centerline (x-y plane) called ThetaOffset.

# Import external libraries
import numpy as np
import time

# Import internal programs
import L2_color_target as ct
import L2_kinematics as kin
import L2_speed_control as sc
import L2_inverse_kinematics as inv
import L2_log as log
#import L2_joint as joint

# initialize variables for control system
t0 = 0
t1 = 1
e00 = 0
e0 = 0
e1 = 0
dt = 0
de_dt = np.zeros(2) # initialize the de_dt
count = 0

# initialize variables for color tracking
color_range = np.array([[0, 185, 100], [175, 220, 175]]) # Input your HSV choices
thetaOffset = 0 # the measured offset of target (degrees)
x = 0 # target center location (pixels)

while(1):
    ts0 = time.time() # check time
    colorTarget = ct.colorTarget(color_range) # use color tracking to generate target (x,y,radius)
    #print(colorTarget)
    ts1 = time.time() - ts0 # check image processing time
    log.tmpFile(ts1, "cvSpeed.txt") 
    if colorTarget != None:
        x = colorTarget[0]  # assign the x pixel location of the target
        if x != None:
            thetaOffset = ct.horizLoc(x) # grabs the angle of the target in degrees
    #joint.one(thetaOffset) # request pointer to point to the target.
    myThetaDot = thetaOffset * 3.14/180 *2 # attempt centering in 0.5 seconds
    print("x, pixels:", x, "T-offset:", thetaOffset, "processing (s):", round(ts1,4), "myTD (rad/s):", round(myThetaDot,3))
    myXDot = 0 # freeze the forward driving
    
    # BUILD SPEED TARGETS ARRAY
    A = np.array([ myXDot, myThetaDot ])
    pdTargets = inv.convert(A) # convert from [xd, td] to [pdl, pdr]
    kin.getPdCurrent() # capture latest phi dots & update global var
    pdCurrents = kin.pdCurrents # assign the global variable value to a local var
   
    # UPDATES VARS FOR CONTROL SYSTEM
    t0 = t1  # assign t0
    t1 = time.time() # generate current time
    dt = t1 - t0 # calculate dt
    e00 = e0 # assign previous previous error
    e0 = e1  # assign previous error
    e1 = pdCurrents - pdTargets # calculate the latest error
    de_dt = (e1 - e0) / dt # calculate derivative of error
    
    # CALLS THE CONTROL SYSTEM TO ACTION
    sc.driveClosedLoop(pdTargets, pdCurrents, de_dt)  # call the control system
    # sc.driveOpenLoop(pdTargets)  # call the control system
    time.sleep(0.005) # very small delay.
