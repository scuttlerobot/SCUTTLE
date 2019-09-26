# L3_drivingPatterns.py
# Team Number:
# Hardware TM:
# Software TM:
# Date:
# Code purpose: 
# indicate d1 and d2 distances:

# Import Internal Programs
import L2_speed_control as sc
import L2_inverse_kinematics as inv

# Import External programs
import numpy as np
import time

def task2():
	myVelocities = np.array([1, 1]) #input your first pair
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(2) # input your duration (s)
	
	myVelocities = np.array([1, 1]) #input your 2nd pair
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(2) # input your duration (s)
	
	myVelocities = np.array([1, 1]) #input your 3rd pair
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(2) # input your duration (s)
	
	myVelocities = np.array([1, 1]) #input your 4th pair
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(2) # input your duration (s)
	
	myVelocities = np.array([1, 1]) #input your 5th pair
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(2) # input your duration (s)
	
	myVelocities = np.array([1, 1]) #input your 6th pair
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(2) # input your duration (s)
	
while 1:
    task2()
    time.sleep(0.2)
