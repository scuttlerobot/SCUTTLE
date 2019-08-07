import cv2
import numpy as np

class MyFilter:

    def process(self, img):

        h = img.shape[0]
        w = img.shape[1]

        w2 = int(w/2)
        h2 = int(h/2)

        cv2.line(img, (int(w/4), h2), (int(3*(w/4)), h2), (0xff, 0, 0), thickness=3)
        cv2.line(img, (w2, int(h/4)), (w2, int(3*(h/4))), (0xff, 0, 0), thickness=3)

        return img

def init_filter():
    f = MyFilter()
    return f.process
