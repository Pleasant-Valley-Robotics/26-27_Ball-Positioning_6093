import cv2
import numpy as np

import converter

img: np.ndarray
#img = cv2.imread('images/image1.jpg')
img = converter.getVideoFrame("video1.mp4", 50)

def getCurrentImage():
    return img

def clickEvent(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        cv2.circle(getCurrentImage(), (x, y), 15, (255, 0, 0), -1)
        cv2.imshow("image", getCurrentImage())

if __name__ == "__main__":
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image", 1200, 800)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', clickEvent)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


