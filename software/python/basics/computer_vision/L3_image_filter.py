#FILTER

import cv2
import numpy as np

v1_min = 0     # Minimum H value
v2_min = 180     # Minimum S value
v3_min = 130    # Minimum V value

v1_max = 10     # Maximum H value
v2_max = 255     # Maximum S value
v3_max = 255    # Maximum V value

width  = 240  # please attempt to put back into the function
height = 160

#    RGB or HSV

filter = 'HSV'  # Use HSV to describe pixel color values

color_range = ((0,180,130),(10,255,255))

class MyFilter:

    def colorTracking(self, image, range=color_range, min_size=6, max_size=6):

        image = cv2.resize(image,(width,height)) # resize the image

        if filter == 'RGB':
            frame_to_thresh = image.copy()
        else:
            frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # convert image to hsv colorspace RENAME THIS TO IMAGE_HSV

        with open('/tmp/h_min') as h_min_file:
            h_min_file.seek(0)
            try:
                h_min = int(h_min_file.read())
            except:
                h_min = 0

        with open('/tmp/s_min') as s_min_file:
            s_min_file.seek(0)
            try:
                s_min = int(s_min_file.read())
            except:
                s_min = 0

        with open('/tmp/v_min') as v_min_file:
            v_min_file.seek(0)
            try:
                v_min = int(v_min_file.read())
            except:
                v_min = 0
        with open('/tmp/h_max') as h_max_file:
            h_max_file.seek(0)
            try:
                h_max = int(h_max_file.read())
            except:
                h_max= 0
        with open('/tmp/s_max') as s_max_file:
            s_max_file.seek(0)
            try:
                s_max = int(s_max_file.read())
            except:
                s_max= 0
        with open('/tmp/v_max') as v_max_file:
            v_max_file.seek(0)
            try:
                v_max = int(v_max_file.read())
            except:
                v_max= 0

        color_range = (((h_min), (s_min), (v_min)),((h_max), (s_max), (v_max)))
        # print(color_range)

        # Copy and paste this section into the MJPEG streamer file to make
        # your video output agree with the target capturing function.
        #-------------------------------------------------------------------------
        thresh = cv2.inRange(frame_to_thresh, color_range[0], color_range[1]) # Converts a 240x160x3 matrix to a 240x160x1 matrix
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
            # M = cv2.moments(c)
            # center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))  # defines a circle around the largest target area
            center = (int(x), int(y))  # defines a circle around the largest target area

            if radius > min_size:

                cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2) #draw a circle on the image
                cv2.circle(image, (int(x), int(y)), 3, (0, 0, 0), -1) # draw a dot on the target center
                cv2.circle(image, (int(x), int(y)), 1, (255, 255, 255), -1) # draw a dot on the target center

                # cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)

                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255,255,255),1,cv2.LINE_AA)
        # -----------------------------------------------------------------------------------------------------
        # else:
        #     return None

#    def build_image():
        image_height, image_width, channels = image.shape   # get image dimensions

        spacer = np.zeros((image_height,3,3), np.uint8)
        spacer[:,0:width//2] = (255,255,255)      # (B, G, R)

        # make 3 images to have the same colorspace, for combining
        thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        # border1 = np.array() # use H, height of photos to define
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        # border2 = np.array() # same as above
        # all = np.hstack((image, spacer, thresh, spacer, mask))
        all = np.vstack((image, thresh, mask))

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
