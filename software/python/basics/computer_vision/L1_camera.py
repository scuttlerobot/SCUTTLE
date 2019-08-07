import cv2

width  = 240
height = 160

camera = cv2.VideoCapture(0)

def takepic(size=(width, height)):

    ret, image = camera.read()
    if not ret:
        return None

    image = cv2.resize(image,size) # resize the image

    return image
