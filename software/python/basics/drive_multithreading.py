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

axes = np.zeros(16) #number of elements returned by gamepad

def loop_speak( ID ):
    while(1):
        myStringA = "hello everybody I'm a multi-threading scuttle"
        myStringX = "you pressed X!"
        myStringB = "firing the missiles"
        signals = gp.getGP()
        if signals[6]==1: # A button is pressed
            t2s.say(myStringA)
        if signals[7]==1: # x button is pressed
            t2s.say(myStringX)
        if signals[5]==1: # x button is pressed
            t2s.say(myStringB)
        time.sleep(0.1)

def loop_drive( ID ):
    while(1):
            #get the latest target phi_dots from inverse kinematics
            phis = inv.get_phis() # populates target phi dots, targets
            print("phi dot left:", phis[0])
            #call the speed control system to action:
            sc.driveOpenLoop(phis[0],phis[1])
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
        t.join()
        t2.join()

main()
