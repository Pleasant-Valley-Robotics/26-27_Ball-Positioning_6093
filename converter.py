import cv2
import numpy as np

import grapher

videoPath = "video1.mp4"

fileOutPath = "data.txt"

blur = 11

lowerYellow = np.array([20, 100, 100])
upperYellow = np.array([30, 255, 255])

def findBallCenter(image) -> tuple[int, int] | None:
    if image is None:
        print("Error: Image could not be read.")
        return None

    blurred = cv2.GaussianBlur(image, (blur, blur), 0)

    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lowerYellow, upperYellow)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    moments = cv2.moments(mask)

    if moments["m00"] != 0:
        centerX = int(moments["m10"] / moments["m00"])
        centerY = int(moments["m01"] / moments["m00"])

        #cv2.circle(image, (centerX, centerY), 10, (0, 0, 255), -1)
        #cv2.imwrite("detected_center.png", image)

        return centerX, centerY

def computeVideo(videoPath: str) -> tuple[np.ndarray, np.ndarray] | None:
    capture = cv2.VideoCapture(videoPath)
    if not capture.isOpened():
        print("Error: could not open video")
        exit(1)

    xPoints: np.ndarray = np.array([])
    yPoints: np.ndarray = np.array([])

    while capture.isOpened():
        ret, frame = capture.read()

        if ret == False:
            print("Reached the end of the video or failed to load frame.")
            break

        position = findBallCenter(frame)

        if position is None:
            print("Can't find position of ball!")
            continue

        xPoints = np.append(xPoints, position[0])
        yPoints = np.append(yPoints, position[1])
        
    capture.release()

    return xPoints, yPoints

def loadImage(imagePath: str):
    return cv2.imread(imagePath)

if __name__ == "__main__":
    #centerX, centerY = findBallCenter("images/testImage.png")
    #print(f"Center coordinates found at: X={centerX}, Y={centerY}")

    #xPoints, yPoints = grapher.loadData(fileOutPath)

    output = computeVideo(videoPath)

    if output == None:
        print("Video ran into an error")
        exit()

    xPoints, yPoints = output

    grapher.writeData(fileOutPath, xPoints, yPoints)

    grapher.graphPoints(xPoints, yPoints)
    #grapher.graphPoints(np.array([centerX]), np.array([centerY]))


cv2.destroyAllWindows()