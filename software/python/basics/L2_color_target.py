#!/usr/bin/python3

# This program takes an image, applies filters with openCV, and returns
# a color target if located in the image.  The target parameters are (x,y,radius).

# Import external libraries
import cv2
import numpy as np

# Import internal programs
import L1_camera as cam

width = 120                                                 # width of image being processed (pixels)
color_range = np.array([[0, 0, 0], [255, 255, 255]])        # enter values here if running standalone program.


# This function searches an image for an object of the specified color.  Returns array containing [x, y, radius] in pixels.
def colorTarget(color_range=((0, 0, 0), (255, 255, 255))):

    image = cam.newImage()
    if filter == 'RGB':
        frame_to_thresh = image.copy()
    else:
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                # convert image to hsv colorspace RENAME THIS TO IMAGE_HSV

    thresh = cv2.inRange(frame_to_thresh, color_range[0], color_range[1])
    mask = thresh

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]    # generates number of contiguous "1" pixels
    if len(cnts) == 0:                                                                      # begin processing if there are "1" pixels discovered
        return np.array([None, None, 0])
    else:
        c = max(cnts, key=cv2.contourArea)                                                  # return the largest target area
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 4:
            return np.array([round(x, 1), round(y, 1), round(radius, 1)])


def horizLoc(target_x):                             # generate an estimate of the angle of the target from center
    if target_x is not None:
        viewAngle = 90                              # camera view, degrees
        ratio = target_x / width                    # divide by pixels in width
        wrtCenter = ratio - 0.5                     # offset.  Now, positive value = right, negative = left
        targetTheta = -1 * wrtCenter * viewAngle    # scale the value roughly to degrees
        return int(targetTheta)
    else:
        return None


if __name__ == "__main__":
    while True:
        target = colorTarget(color_range)           # grab target x, y, radius
        x = target[0]
        radius = target[2]
        if x is None:
            print("no target located.")
        else:
            targetTheta = horizLoc(x)
            print(targetTheta)
            print("x:", x, "\t", "radius:", radius)
