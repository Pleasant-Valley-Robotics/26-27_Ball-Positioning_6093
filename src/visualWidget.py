import cv2
import numpy as np
from pathlib import Path

import src.converter as converter

class Grabber:
    fileName: str = "fullTest.mp4"

    img: np.ndarray

    windowName = "image"

    shown: bool = False

    def setFileName(self, name:str):
        self.fileName = name

    def getFilePath(self) -> Path:
        return converter.getVideoPath(self.fileName)

    def getCurrentImage(self):
        return self.img

    def loadVideo(self, desiredFrame: int):
        self.img = converter.getVideoFrame(self.getFilePath(), desiredFrame)
        cv2.imshow(self.windowName, self.getCurrentImage())

    def openWindow(self):
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.windowName, 1200, 800)
        self.imageShown = True
        
    def closeWindow(self):
        if self.imageShown:
            cv2.destroyAllWindows()
            self.imageShown = False
    

class PointGrabber(Grabber):
    #img = cv2.imread('images/image1.jpg')
    #img = converter.getVideoFrame("videos/fullTest.mp4", 100)
    
    points: list[np.ndarray] = []
    
    def __init__(self) -> None:
        ...

    #def setFileName(self, name: str):
    #    return super().setFileName(name + ".mp4")
    
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

class FrameGrabber(Grabber):
    currentFrame: int = 0

    jumpDist: int = 100

    hasFrame: bool = False

    def __init__(self) -> None:
        pass

    #def setFileName(self, name: str):
    #    return super().setFileName(name + ".mp4")

    def changeFrame(self, ammount: int):
        self.currentFrame += ammount
        self.loadVideo(self.currentFrame)

    def setFrame(self, start: int):
        self.currentFrame = start
        self.loadVideo(self.currentFrame)

    def getFrame(self, startingFrame: int):
        self.openWindow()
        self.setFrame(startingFrame)
        self.hasFrame = False
        while not self.hasFrame:
            key = cv2.waitKeyEx(1)
            if key == 32:
                self.hasFrame = True

            # left arrow
            if key == 65361:
                self.changeFrame(-self.jumpDist)
            # right arrow
            if key == 65363:
                self.changeFrame(self.jumpDist)

            if key == ord('n'):
                self.changeFrame(-self.jumpDist // 4)
            if key == ord('m'):
                self.changeFrame(self.jumpDist // 4)

            # comma
            if key == 44:
                self.changeFrame(-1)
            # period
            if key == 46:
                self.changeFrame(1)

            if key == 27:
                cv2.destroyAllWindows()
                "Exiting early..."
                exit(1)

        while not cv2.waitKey(30) == 27:
            ...

        self.closeWindow()

        return self.currentFrame

if __name__ == "__main__":
    """
    grabber = PointGrabber()
    grabber.setFileName("fullTest.mp4")
    grabber.openWindow()
    grabber.loadVideo(10)
    points = grabber.getPoints(2)
    grabber.loadVideo(100)
    points = grabber.getPoints(2)
    grabber.closeWindow()
    print(points)
    """

    grabber = FrameGrabber()
    grabber.setFileName("fullTest.mp4")
    frame = grabber.getFrame(200)
    print(frame)