# This program demonstrates importing of other python files and
# calling functions from child files.
# last updated 2019.05.23

# IMPORT EXTERNAL ITEMS
import time
import numpy as np # for handling matrices
import threading # only used for threading functions
import math
# IMPORT INTERNAL ITEMS
import L2_speed_control as sc # closed loop control. Import speed_control for open-loop
import L2_inverse_kinematics as inv #calculates wheel parameters from chassis
import L2_kinematics as kin    # calculates chassis parameters from wheels
import L2_log # log live data to local files
import L1_gamepad as gp
import L1_encoder as enc
import L1_text2speech as t2s # for speaking by aux port
# import L2_obstacle as obs

def loop_speak( ID ):
    while(1):
        myStringA = "I am scuttle robot"
        myStringX = "the future of meka tronics"
        myStringB = "Special delivery"
        myStringY = "gig em aggies"
        signals = gp.getGP()
        if signals[6]==1: # A button is pressed
            print("you pressed A.")
            t2s.say(myStringA)
        if signals[7]==1: # x button is pressed
            t2s.say(myStringX)
        if signals[5]==1: # x button is pressed
            t2s.say(myStringB)
        if signals[4]==1: #
            t2s.say(myStringY)
        time.sleep(0.05)

def loop_drive( ID ):
    
    t0 = 0
    t1 = 1
    e00 = 0
    e0 = 0
    e1 = 0
    dt = 0
    de_dt = np.zeros(2) # initialize the de_dt
    
    while(1):

        # THIS CODE IS FOR OPEN AND CLOSED LOOP control
        pdTargets = inv.getPdTargets() # populates target phi dots from GamePad
        kin.getPdCurrent() # capture latest phi dots & update global var
        pdCurrents = kin.pdCurrents # assign the global variable value to a local var

        # The following block is for continuous driving
        # myThetaDot = 1.5 # target, rad/s
        # myXDot = 0.2 # target, m/sc
        # A = np.array([myXDot, myThetaDot])
        # myPhiDots = inv.convert(A)
        
        t0 = t1  # assign t0
        t1 = time.time() # generate current time
        dt = t1 - t0 # calculate dt
        #print("dt = ", round(dt,3))
        e00 = e0 # assign previous previous error
        e0 = e1  # assign previous error
        e1 = pdCurrents - pdTargets # calculate the latest error
        de_dt = (e1 - e0) / dt # calculate derivative of error
        sc.driveClosedLoop(pdTargets, pdCurrents, de_dt)  # call the control system
        if (pdCurrents[0] > pdTargets[0]):
            print(count)
            break
    log.csv_write([count, pdCurrents[0], pdCurrents[1]])

def loop_scan( ID ):
    while(1):
            # d = obs.nearest_point() #returns the distance and the y-value of nearest obstacle
            # #print("nearest point:", d)
            # if d[0] < 0.15: #if the nearest obstacle less than 10cm
            #         t2s.say("NO")
        time.sleep(0.1)

def main():

        print("starting the main fcn")
        threads = []  # create an object for threads

        t = threading.Thread( target=loop_speak, args=(1,) ) # make 1st thread object
        threads.append(t)
        t.start()
        print("started thread1")

        t2 = threading.Thread( target=loop_drive, args=(2,) ) # make 2nd thread object
        threads.append(t2)
        t2.start()
        print("started thread2")

        t3 = threading.Thread( target=loop_scan, args=(3,) ) # make 2nd thread object
        threads.append(t3)
        t3.start()
        print("started thread3")

 #should have while loop to run 'joins' not the threaded functions
        t.join()
        t2.join()
        t3.join()

main()
