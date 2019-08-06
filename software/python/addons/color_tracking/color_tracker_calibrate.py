# This code is to visually calibrate the color range
# for color tracking on the SCUTTLE robot.

# Please make sure X11 forwarding is enabled
# when running this code.

import cv2
import argparse
import numpy as np
import os

width  = 240
height = 160

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

#    Color Range, described in HSV

v1_min = 30     # Minimum H value
v2_min = 20     # Minimum S value
v3_min = 245    # Minimum V value

v1_max = 43     # Maximum H value
v2_max = 98     # Maximum S value
v3_max = 255    # Maximum V value

#    RGB or HSV

filter = 'HSV'  # Use HSV to describe pixel color values

def main():

	camera = cv2.VideoCapture(0)

	camera.set(3, width)
	camera.set(4, height)

	while True:

		ret, image = camera.read()
		if not ret:
			break

		image = rotateImage(image,180)

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
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			if radius > 6:

				cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
				cv2.circle(image, center, 3, (0, 0, 255), -1)
				cv2.putText(image,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
				cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)

		# cv2.imshow("Original", image)
		# cv2.imshow("Thresh", thresh)
		# cv2.imshow("Mask", mask)

		return image

if __name__ == '__main__':
	main()
