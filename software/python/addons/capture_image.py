# this program is the barebones commands to capture an image with opencv2.
# if you want to run these commands in command line, first enter "sudo python3"

import cv2                          # import the opencv library
capture = cv2.VideoCapture(0)       # connect to the camera - may need 0 or 1 channel
ret, frametmp = capture.read()      # capture a frame
cv2.imwrite("frame1.png", frametmp) # store the captured data to a file with .png extension

# to quit python3, type: "quit()"
