# color_tracking_v1.py
# usb camera: Microsoft HD-3000 target: orange basketball
# This program was designed to have SCUTTLE following a basketball.
# The calibration was made in a brightly lit indoor environment.
# Video demo: https://youtu.be/9t1XHcomlIs

print("loading libraries for color tracking...")
import cv2
import argparse
import numpy as np
import os
import time


print("loading rcpy.")
# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy
import rcpy.motor as motor
print("finished loading libraries.")
#    Camera

camera_input = 0

size_w  = 240   #this is the pixel width
size_h = 160	#this is the pixel height

#    Color Range, described in HSV

v1_min = 22
v2_min = 82
v3_min = 75

v1_max = 25
v2_max = 255
v3_max = 255

#    RGB or HSV

filter = 'HSV'

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def main():

    camera = cv2.VideoCapture(camera_input)
    camera.set(3, size_w)
    camera.set(4, size_h)

    tc = 70     # Too Close
    tf = 6      # Too Far
    tp = 65     # Target Pixels

    band = 50   #range of x considered to be centered

    x = 0  # will describe target location left to right
    y = 0  # will describe target location bottom to top

    radius = 0  # estimates the radius of the detected target

    duty_l = 0 # initialize motor with zero duty cycle
    duty_r = 0 # initialize motor with zero duty cycle

    print("initializing rcpy...")
    rcpy.set_state(rcpy.RUNNING)
    print("finished initializing rcpy.")

    try:

        while rcpy.get_state() != rcpy.EXITING:

            if rcpy.get_state() == rcpy.RUNNING:

                scale_t = 1.3	# a scaling factor for speeds
                scale_d = 1.3	# a scaling factor for speeds

                motor_r = 2 	# Right Motor assigned to #2
                motor_l = 1 	# Left Motor assigned to #1

                ret, image = camera.read()

                image = rotateImage(image,180)

                height, width, channels = image.shape

                if not ret:
                    break

                if filter == 'RGB':
                    frame_to_thresh = image.copy()
                else:
                    frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

                kernel = np.ones((5,5),np.uint8)
                mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
                center = None

                if len(cnts) > 0:

                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)

                    radius = round(radius, 2)

                    x = int(x)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    # handle centered condition
                    if x > ((width/2)-(band/2)) and x < ((width/2)+(band/2)):

                        dir = "driving"

                        if radius >= tp:    # Too Close

                            case = "too close"

                            duty = -1 * ((radius-tp)/(tc-tp))


                        elif radius < tp:   # Too Far

                            case = "too far"

                            duty = 1 - ((radius - tf)/(tp - tf))
                            duty = scale_d * duty

                        duty_r = duty
                        duty_l = duty

                    else:
                        case = "turning"

                        duty_l = round((x-0.5*width)/(0.5*width),2)       # turn left
                        duty_l = duty_l*scale_t

                        duty_r = round((0.5*width-x)/(0.5*width),2)
                        duty_r = duty_r*scale_t

                    if duty_r > 1:
                        duty_r = 1

                    elif duty_r < -1:
                        duty_r = -1

                    if duty_l > 1:
                        duty_l = 1

                    elif duty_l < -1:
                        duty_l = -1

                    duty_l = round(duty_l,2)
                    duty_r = round(duty_r,2)

                    print(case, "\tradius: ", round(radius,1), "\tx: ", round(x,0), "\t\tL: ", duty_l, "\tR: ", duty_r)

                    motor.set(motor_l, duty_l)
                    motor.set(motor_r, duty_r)

                motor.set(motor_l, duty_l)
                motor.set(motor_r, duty_r)

            elif rcpy.get_state() == rcpy.PAUSED:
                pass

    except KeyboardInterrupt: # condition added to catch a "Ctrl-C" event and exit cleanly
        rcpy.set_state(rcpy.EXITING)
        pass

    finally:

    	rcpy.set_state(rcpy.EXITING)
    	print("Exiting Color Tracking.")


# exiting program will automatically clean up cape

if __name__ == '__main__':
    main()
