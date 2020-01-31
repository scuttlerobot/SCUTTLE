#!/usr/bin/python3

# This program takes an image, applies filters with openCV, and returns
# a color target if located in the image.  The target parameters are (x,y,radius).

import cv2
import numpy as np
import L1_camera as cam

color_range = ((0, 0, 0), (255, 255, 255))


def colorTarget(color_range=((0, 0, 0), (255, 255, 255))):

    image = cam.newImage()
    if filter == 'RGB':
        frame_to_thresh = image.copy()
    else:
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                            # convert image to hsv colorspace RENAME THIS TO IMAGE_HSV

    thresh = cv2.inRange(frame_to_thresh, color_range[0], color_range[1])

    # apply a blur function
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)                                 # Apply blur
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)                                  # Apply blur 2nd iteration

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]    # generates number of contiguous "1" pixels
    if len(cnts) > 0:                                                                       # begin processing if there are "1" pixels discovered
        c = max(cnts, key=cv2.contourArea)                                                  # return the largest target area
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        return np.array([round(x, 1), round(y, 1), round(radius, 1)])
    else:
        return np.array([None, None, 0])


def horizLoc(target_x):                                         # generate an estimate of the angle of the target from center
    if target_x is not None:
        viewAngle = 90                                          # camera view, degrees
        ratio = target_x / 240                                  # divide by pixels in width
        wrtCenter = ratio - 0.5                                 # offset.  Now, positive = right, negative = left
        targetTheta = -1 * wrtCenter * viewAngle                # scale the value roughly to degrees
        return int(targetTheta)
    else:
        return None


if __name__ == "__main__":
    while True:
        target = colorTarget(color_range)
        # print(x,y, "\t", radius)
        x = target[0]
        if x is None:
            print("no target located.")
        else:
            targetTheta = horizLoc(x)
            print(targetTheta)
