# This program takes an image using L1_camera, applies filters with openCV, and returns
# a color target if located in the image.  The target parameters are (x,y,radius).
# This program requires that opencv2 is installed for python3.

# Import internal programs:
import L1_camera as cam

# Import external programs:
import cv2          # computer vision
import numpy as np  # for handling matrices
import time         # for keeping time

# Define global parameters
color_range = ((5, 135, 85), (25, 235, 215))  # This color range defines the color target

def colorTarget(color_range=((0, 0, 0), (255, 255, 255))): # function defaults to open range if no range is provided
    image = cam.newImage()
    if filter == 'RGB':
        image_hsv = image.copy()
    else:
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    # convert to hsv colorspace

    thresh = cv2.inRange(image_hsv, color_range[0], color_range[1])
    kernel = np.ones((5, 5), np.uint8)                                      # apply a blur function
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)                 # Apply blur
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)                  # Apply blur 2nd iteration

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)[-2]                        # generates number of contiguous "1" pixels
    if len(cnts) > 0:                                           # begin processing if there are "1" pixels discovered
        c = max(cnts, key=cv2.contourArea)                      # return the largest target area
        ((x, y), radius) = cv2.minEnclosingCircle(c)            # get properties of circle around shape
        targ = np.array([int(x), int(y),                        # return x, y, radius, of target 
                round(radius, 1)])
        return targ
    else:
        return np.array([None, None, 0])

def getAngle(x):                         # check deviation of target from center
    if x is not None:
        ratio = x / 240                  # divide by pixels in width
        offset = -2*(ratio - 0.5)        # offset.  Now, positive = left, negative = right
        offset_x = round(offset,2)       # perform rounding
        return (offset_x)
    else:
        return None

# THIS SECTION ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    while True:
        target = colorTarget(color_range) # generate a target
        print(target)
        x = target[0]
        if x is None:
            print("no target located.")
        else:
            x_offset = getAngle(x)
            print("Target x location: ", x_offset)
        time.sleep(0.1) # short delay
