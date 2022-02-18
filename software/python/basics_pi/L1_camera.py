# This program retrieves an image from the usb camera.
# This requires installation of opencv2 for python.
# If it is successful, it prints the dimensions of the captured image.

# Import external libraries
import cv2  # opencv library for capturing & processing images
import time # time library

# Initialize important vars
width  = 240                      # desired width in pixels
height = 160                      # desired height in pixels
# width = 120                         # desired width in pixels
# height = 80                         # desired height in pixels
camera = cv2.VideoCapture(0)        # Take images from the camera assigned as "0"

# A function to capture an image & return all pixel data
def newImage(size=(width, height)):
    ret, image = camera.read()          # return the image as well as ret
    if not ret:                         # (ret is a boolean for returned successfully?)
        print("NO IMAGE")
        return None                     # (return an empty var if the image could not be captured)
    image = cv2.resize(image, size)     # reduce size of image
    return image

# THIS SECTION ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    while True:
        image = newImage()                  # capture an image from the usb cam
        time.sleep(0.5)                     # short delay
        print("Image shape: ", image.shape) # print info about the image (height, width, colorspace)
