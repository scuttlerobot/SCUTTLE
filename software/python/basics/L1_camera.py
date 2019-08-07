# This file retrieves an image from the usb camera.
import numpy as np
import cv2

width  = 240
height = 160
camera = cv2.VideoCapture(0) # This will take images only from the camera assigned as "0"

def newImage(size=(width, height)):
    ret, image = camera.read()
    if not ret:
        return None
    image = cv2.resize(image,size) # resize the image
    return image
    
# UNCOMMENT THE SECTION BELOW TO RUN AS A STANDALONE PROGRAM
while 1:
    image = newImage()
    print(image.shape) #print info about the image (height, width, colorspace)
