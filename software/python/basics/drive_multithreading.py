# this program demonstrates importing of other python files and
# calling functions from child files.
# last updated 2019.05.23

# IMPORT EXTERNAL ITEMS
import time
import numpy as np # for handling matrices
import text2speech_ex2 as t2s #for speaking by aux port
import threading # only used for threading functions
# IMPORT INTERNAL ITEMS
import encoder_ex2 as enc # for encoders
import speed_control as sc # for generating speed commands
import inverse_kinematics as inv
import gamepad_ex2 as gp # TEMPORARILY IMPORT THIS FILE ONLY!
import kinematics as kin
import repel as repel

axes = np.zeros(16) #number of elements returned by gamepad

def loop_speak( ID ):
    while(1):
        myStringA = "hello everybody, I am scuttle robot"
        myStringX = "do you smell what the rock is cooking?"
        myStringB = "Special delivery"
        myStringY = "gig em aggieees"
        signals = gp.getGP()
        if signals[6]==1: # A button is pressed
            t2s.say(myStringA)
        if signals[7]==1: # x button is pressed
            t2s.say(myStringX)
        if signals[5]==1: # x button is pressed
            t2s.say(myStringB)
        if signals[4]==1: #
            t2s.say(myStringY)
        time.sleep(0.05)

def loop_drive( ID ):
    while(1):
            #get the latest target phi_dots from inverse kinematics
            phis = inv.get_phis() # populates target phi dots, targets
            #print("phi dot left:", phis[0])

            d = repel.nearest_point() #returns the distance and the y-value of nearest obstacle
            print("nearest point:", d)
            phi_influence = inv.phi_influence(d[1]) #send the y-value of nearest point to this fcn.
            phis = phis + phi_influence #combine the obstacle influence with phis
            
            #call the speed control system to action:
            sc.driveOpenLoop(phis[0],phis[1])
            time.sleep(0.1)
            motion = kin.getMotion() # populate thetaDot & xDot
            #print("thetadot,xdot", motion)

def loop_scan( ID ):
    while(1):
            # d = repel.nearest_point() #returns the distance and the y-value of nearest obstacle
            # print("nearest point:", d)
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

        t.join()
        t2.join()
        t3.join()
main()
