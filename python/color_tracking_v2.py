import cv2
import argparse
import numpy as np
import os
import time

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy
import rcpy.motor as motor

#    Camera

camera_input = 0

size_w  = 240
size_h = 160

#    Color Range

v1_min = 7
v2_min = 178
v3_min = 84

v1_max = 16
v2_max = 255
v3_max = 255

'''
v1_min = 0
v2_min = 14
v3_min = 163

v1_max = 61
v2_max = 255
v3_max = 255
'''
#    RGB or HSV

filter = 'HSV'

def main():

    camera = cv2.VideoCapture(camera_input)
    camera.set(3, size_w)
    camera.set(4, size_h)

    tc = 70     # Too Close
    tf = 6      # Too Far
    tp = 65     # Target Pixels

    band = 50   #range of x considered to be centered

    x = 0
    y = 0

    radius = 0
    dir = "center"

    duty_l = 0
    duty_r = 0

#    rcpy.set_state(rcpy.RUNNING)

    try:

        while 1:

            if True:

                scale_t = 1.3
                scale_d = 1.3

                motor_r = 2 	# Right Motor
                motor_l = 1 	# Left Motor

                ret, image = camera.read()

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

                    cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(image, center, 3, (0, 0, 255), -1)
	            cv2.putText(image,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
	            cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)


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

	        cv2.imshow("Original", image)
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Mask", mask)

            elif rcpy.get_state() == rcpy.PAUSED:
                # do other things
                pass

    except KeyboardInterrupt:
    # Catch Ctrl-C
        pass

    finally:

    # say bye
        print("\nBye Beaglebone!")

# exiting program will automatically clean up cape

if __name__ == '__main__':
    main()
