import cv2
import numpy as np
from pathlib import Path

import converter

class PointGrabber:
    imgName: str = "fullTest.mp4"
    img: np.ndarray
    #img = cv2.imread('images/image1.jpg')
    #img = converter.getVideoFrame("videos/fullTest.mp4", 100)
    
    points: list[np.ndarray] = []
    
    imageShown: bool = False
    
    windowName = "image"
    
    def __init__(self) -> None:
        ...
    
    def setImageName(self, name:str):
        self.imgName = name
    
    def getImgPath(self) -> Path:
        return converter.getVideoPath(self.imgName)
    
    def loadImage(self, desiredFrame: int):
        self.img = converter.getVideoFrame(self.getImgPath(), desiredFrame)
        cv2.imshow(self.windowName, self.getCurrentImage())
    
    def getCurrentImage(self):
        return self.img
    
    def openWindow(self):
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.windowName, 1200, 800)
        self.imageShown = True
        
    def closeWindow(self):
        if self.imageShown:
            cv2.destroyAllWindows()
            self.imageShown = False
    
    def addPoint(self, x: int, y: int):
        self.points.append(np.array([x, y]))
    
    def getPoints(self, pointNum):
        if not self.imageShown:
            print("No image to get points from")
            return None
        cv2.setMouseCallback(self.windowName, self.clickEvent)
        self.points = []
        while len(self.points) < pointNum:
            key = cv2.waitKey(50)
            if key == 27:
                cv2.destroyAllWindows()
                exit(1)
            if cv2.getWindowProperty(self.windowName, cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyAllWindows()
                exit(1)
        return self.points
    
    def clickEvent(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            #print(x, y)
            self.addPoint(x, y)
            cv2.circle(self.getCurrentImage(), (x, y), 15, (255, 0, 0), -1)
            cv2.imshow("image", self.getCurrentImage())

if __name__ == "__main__":
    grabber = PointGrabber()
    grabber.setImageName("fullTest.mp4")
    grabber.openWindow()
    grabber.loadImage(10)
    points = grabber.getPoints(2)
    grabber.loadImage(100)
    points = grabber.getPoints(2)
    grabber.closeWindow()
    print(points)