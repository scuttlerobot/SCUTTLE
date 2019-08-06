# This program takes the [x,y,radius] parameters of a target and
# generates movement commands to follow it.
# The calibration was made in a brightly lit indoor environment.
# Video demo: https://youtu.be/9t1XHcomlIs

# Color Tracking libraries
import color_target_ex1	as ct 	# for capturing camera info
import argparse         		# For fetching user arguments
import numpy as np      	

# Camera
size_w  = 240   # Resized image width. This is the image width in pixels.
size_h = 160	# Resized image height. This is the image height in pixels.

myCal = np.array([30,20,245,43,98,255]) #example calibration tuned for basketball
# getFrame requires an argument color_cal consisting of minimum H,S,V followed by high H,S,V

# a function to produce target x_dot and theta_dot (fwd and turning)
def track():

    tc = 70     # Too Close     - Maximum pixel size of object to track
    tf = 6      # Too Far       - Minimum pixel size of object to track
    tp = 65     # Target Pixels - Target size of object to track
    band = 50   # range of x considered to be centered
	
	target = ct.getFrame(myCal)  # capture a frame from camera
    x = target[0]  # will describe target location left to right
    y = target[1]  # will describe target location bottom to top
    radius = target[2]  # estimates the radius of the detected target

	scale_xd = 1.3	# a scaling factor for x_dot speeds
	scale_td = 1.3	# a scaling factor for theta_dot speeds

	# handle centered condition (approach, stall, or reverse?)
	if x > ((width/2)-(band/2)) and x < ((width/2)+(band/2)):       # If target center point is in middle
		dir = "driving"
		if radius >= tp:    # Too Close
			case = "too close"
			xd_request = -1 * ((radius-tp)/(tc-tp))
		elif radius < tp:   # Too Far
			case = "too far"
			xd_request = 1 - ((radius - tf)/(tp - tf))
			x_duty = scale_d * duty
			
	xd_request = scale_xd * xd_request 	# apply scaling to fwd/back movement
	
	# handle the turning condition (left or right)
	else:
		case = "turning"
		duty_l = round((0.5*width-x)/(0.5*width),2)     # a ratio describing how left-biased is target wrt center
		td_request = duty_l*scale_td					# generate a theta_dot request.  positive gives left turn
