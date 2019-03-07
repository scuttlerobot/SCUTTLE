# python dynamic_color_tracking.py --filter HSV --webcam

import cv2
import time
import argparse
import numpy as np

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy
import rcpy.motor as motor

#    Camera

camera_input = 0

width  = 240
height = 160

#    Color Range

v1_min = 0
v2_min = 161
v3_min = 42

v1_max = 33
v2_max = 253
v3_max = 255


#    RGB or HSV

filter = 'HSV'


motor_r = 2 	#Right Motor?
motor_l = 1 	#Left Motor?

def main():

    rcpy.set_state(rcpy.RUNNING)

    camera = cv2.VideoCapture(camera_input)
    camera.set(3, width)
    camera.set(4, height)

    while rcpy.get_state() != rcpy.EXITING:

        if rcpy.get_state() == rcpy.RUNNING:

            time.sleep(0.1)

            duty_l = 0
            duty_r = 0

            ret, image = camera.read()
            if filter == 'RGB':
                frame_to_thresh = image.copy()
            else:
                frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

            kernel = np.ones((5,5),np.uint8)
            mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(image, center, 3, (0, 0, 255), -1)
                    cv2.putText(image,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                    cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)

            else:

                x, y, radius = (width/2), (height/2), 0

    #        print("Location: ", round(x,0)," , ", round(y,0), "\t\t\t Radius: ", round(radius,0))


            if x > 0 and x < 40:                  #--------target is on the left--------

                duty_l = -1       # turn left (reduced spd)
                duty_r =  1
                print("LEFT")

            elif x > 40 and x < 120:               #-------target is centered-----------

                print("CENTER")

                if radius < 60 and radius > 40:  # object is in good range
                    duty_l = 0                   # stop robot
                    duty_r = 0


                elif radius > 40 or radius > 60:  # object is too far
                    duty_l = 1        # forward
                    duty_r = 1

                elif radius > 60:                     # object is too close
                    duty_l = -1        # reverse
                    duty_r = -1

            elif x > 120:                              #------ target is on the right-------

                print("RIGHT")

                duty_l = 1        # turn right (reduced spd)
                duty_r = -1

            elif x > 160:                              # target is beyond right pixels

                print(x, "lol wut")

            motor.set(motor_l, duty_l)
            motor.set(motor_r, duty_r)

        elif rcpy.get_state() == rcpy.PAUSED:

            # set motors to free spin
            motor.set_free_spin(channel)
            d = 0

if __name__ == '__main__':
    main()

