# This file is referenced by mjpg streamer to filter images before creating a live feed.
# After mjpg streamer is initiated, it sends a feed to 192.168.8.1:8090 for viewing in browser
# the myFilter class should be updated to match any changes made in the L2_color_target.py

import cv2
import numpy as np

v1_min = 0       # Minimum H value
v2_min = 180     # Minimum S value
v3_min = 130     # Minimum V value
v1_max = 10      # Maximum H value
v2_max = 255     # Maximum S value
v3_max = 255     # Maximum V value

width  = 240  # please attempt to put back into the function
height = 160

class MyFilter:

    def colorTracking(self, image):

        image = cv2.resize(image,(width,height)) # resize the image

        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # convert image to hsv colorspace RENAME THIS TO IMAGE_HSV

        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max)) # Converts a 240x160x3 matrix to a 240x160x1 matrix
        # cv2.inrange discovers the pixels that fall within the specified range and assigns 1's to these pixels and 0's to the others.

        # apply a blur function
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel) # Apply blur
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) # Blur again

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] #generates number of contiguous "1" pixels
        center = None # create a variable for x, y location of target

        if len(cnts) > 0:   # begin processing if there are "1" pixels discovered

            c = max(cnts, key=cv2.contourArea)  # return the largest target area
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))  # defines a circle around the largest target area

            if radius > 6:

                cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2) #draw a circle on the image
                cv2.circle(image, (int(x), int(y)), 3, (0, 0, 0), -1) # draw a dot on the target center
                cv2.circle(image, (int(x), int(y)), 1, (255, 255, 255), -1) # draw a dot on the target center

                # cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)

                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255,255,255),1,cv2.LINE_AA)

        image_height, image_width, channels = image.shape   # get image dimensions

        spacer = np.zeros((image_height,3,3), np.uint8)
        spacer[:,0:width//2] = (255,255,255)      # (B, G, R)

        # make 3 images to have the same colorspace, for combining
        thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        # border1 = np.array() # use H, height of photos to define
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        # border2 = np.array() # same as above
        all = np.hstack((image, spacer, thresh, spacer, mask))

        # cv2.line(all,(image_width,0),(image_width,image_height), (0xff, 0xff, 0xff), thickness=3)
        # cv2.line(all,(image_width*2,0),(image_width*2,image_height), (0xff, 0xff, 0xff), thickness=3)

        # draw text on top of the image for identification
        cv2.putText(all,'Original',(10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(all,'Original',(10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)

        cv2.putText(all,'Thresh',(image_width+10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(all,'Thresh',(image_width+10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)

        cv2.putText(all,'Mask',((image_width*2)+10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(all,'Mask',((image_width*2)+10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)

        return all

def init_filter():  # The function MJPG-Streamer calls.
    f = MyFilter()
    return f.colorTracking
