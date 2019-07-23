# This program demonstrates importing of other python files and
# calling functions from child files.
# last updated 2019.05.23

# IMPORT EXTERNAL ITEMS
import time
import numpy as np # for handling matrices
import text2speech_ex2 as t2s # for speaking by aux port
import threading # only used for threading functions
# IMPORT INTERNAL ITEMS
import speed_control as sc # closed loop control. Import speed_control for open-loop
import inverse_kinematics as inv #calculates wheel parameters from chassis
import kinematics as kin    # calculates chassis parameters from wheels
import log # log live data to local files
import gamepad_ex1 as gp
# import repel as repel

# testing proper global var initialization within inverse kin
#axes = np.zeros(16) #number of elements returned by gamepad

def loop_speak( ID ):
    while(1):
        myStringA = "I am scuttle robot"
        myStringX = "the future of meka tronics"
        myStringB = "Special delivery"
        myStringY = "gig em aggies"
        signals = gp.getGP()
        print(signals)
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
    while(1):
        # THIS CODE IS FOR OPEN AND CLOSED LOOP control
        pdTargets = inv.getPdTargets() # populates target phi dots
        kin.getPdCurrent() # measure latest phi dots & update global variable
        pdCurrent = kin.pdCurrent # assign the global variable value to a local var
        sc.driveOpenLoop(pdTargets[0],pdTargets[1]) #call the speed control system to action:
        #sc.driveClosdedLoop(pdTargets[0], pdCurrent[0])  # testing driveCL with left wheel
        log.writeFiles(pdCurrent)
        print("latest speeds:", pdCurrent)
        time.sleep(0.1)

def loop_scan( ID ):
    while(1):
            # d = repel.nearest_point() #returns the distance and the y-value of nearest obstacle
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

        t.join()
        t2.join()
        t3.join()
main()
