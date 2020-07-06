# this file will let you use your gamepad to drive the SCUTTLE robot


import L2_speed_control as sc
import L2_inverse_kinematics as inv


def manual_nav():
	c = inv.getPdTargets()			
	sc.driveOpenLoop(c)

while 1:
	manual_nav()