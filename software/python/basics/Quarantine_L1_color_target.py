# this program needs to be reviewed - update or delete.

# colorTarget_ex1.py
# usb camera: Microsoft HD-3000 webcam
# This program collects the camera images and outputs color target info.

# Libraries for color tracking
import cv2              # For image capture and processing
import argparse         # For fetching user arguments
import numpy as np      # Kernel

#    Camera
camera_input = 0        # Define camera input. Default=0. 0=/dev/video0
size_w  = 240   # Resized image width. This is the image width in pixels.
size_h = 160	# Resized image height. This is the image height in pixels.
filter = 'HSV'  # Use HSV rather than RGB to describe pixel color values

def getFrame(color_cal):

    camera = cv2.VideoCapture(camera_input)     # Define camera variable
    camera.set(3, size_w)                       # Set width of images that will be retrived from camera
    camera.set(4, size_h)                       # Set height of images that will be retrived from camera
    try:
		ret, image = camera.read()  # Get image from camera
		height, width, channels = image.shape   # Get size of image
		if not ret: 							# was the image returned? 1 = yes
			break
		if filter == 'RGB':                     # If image mode is RGB switch to RGB mode
			frame_to_thresh = image.copy()
		else:
			frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    # Otherwise continue reading in HSV

		# Apply Filters
		thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))   # Find all pixels in color range
		kernel = np.ones((5,5),np.uint8)                            # Set gaussian blur strength.
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)     # Apply gaussian blur
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
		# Pickup Target Data
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]     # Find closed shapes in image
		center = None   # Create variable to store point

		if len(cnts) > 0:   # If more than 0 closed shapes exist, evaluate location

			c = max(cnts, key=cv2.contourArea)              # Get the properties of the largest circle
			((x, y), radius) = cv2.minEnclosingCircle(c)    # Get properties of circle around shape
			radius = round(radius, 2)   # Round radius value to 2 decimals
			x = int(x)          # Cast x value to an integer
			M = cv2.moments(c)  # Gets area of circle contour
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))   # Get center x,y value of circle

		target = np.zeros(3) 	#create a variable to store target info
		target[0] = center(1)	# target x location (of 240)
		target[1] = center(2)	# target y location	(of 160)
		target[2] = radius		# target radius

		return(target)

# uncomment the below section to run as a standalone program
while(1)
	#    Color Range, described in HSV
	color_cal = np.array([30,20,245,43,98,255]) #example calibration tuned for basketball
	# getFrame requires an argument color_cal consisting of minimum H,S,V followed by high H,S,V
	target = getFrame(color_cal)
	print("x_location:", target[0], "y_location:", target[1], "radius:", target[2])
