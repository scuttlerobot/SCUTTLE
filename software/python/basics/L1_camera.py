#!/usr/bin/python3

# This file retrieves an image from the usb camera.

# Import external libraries
import cv2

# Initialize important vars
# width  = 240                      # desired width in pixels
# height = 160                      # desired height in pixels
width = 120                         # desired width in pixels
height = 80                         # desired height in pixels
camera = cv2.VideoCapture(0)        # Take images from the camera assigned as "0"


# A function to capture an image & return all pixel data
def newImage(size=(width, height)):
    ret, image = camera.read()          # return the image as well as ret
    if not ret:                         # (ret is a boolean for returned successfully?)
        print("NO IMAGE")
        return None                     # (return an empty var if the image could not be captured)
    image = cv2.resize(image, size)     # reduce size of image
    return image


if __name__ == "__main__":
    while True:
        image = newImage()
        print(image.shape)          # print info about the image (height, width, colorspace)
