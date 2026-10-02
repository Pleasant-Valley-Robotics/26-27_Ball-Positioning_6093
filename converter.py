import cv2
import numpy as np

import grapher

videoPath = "fullTest.mp4"

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

def getTransformMatrix(pCorner, pXEnd, pYEnd):
    p4 = [
        pXEnd[0] + pYEnd[0] - pCorner[0],
        pXEnd[1] + pYEnd[1] - pCorner[1]
    ]

    srcPoints = np.float32([pCorner, pXEnd, pYEnd, p4]) # type: ignore

    scale = 500

    distCorner = [100, 600]
    distXEnd = [distCorner[0] + scale, distCorner[1]]
    distYEnd = [distCorner[0], distCorner[1] - scale]
    dist4 = [distCorner[0] + scale, distCorner[1] - scale]

    distPoints = np.float32([distCorner, distXEnd, distYEnd, dist4]) # type: ignore

    M = cv2.getPerspectiveTransform(srcPoints, distPoints)
    return M

def rectifyImage(image: np.ndarray, matrix):
    outputSize = (600, 800)
    rectified = cv2.warpPerspective(image, matrix, outputSize)
    return rectified


def computeVideo(videoPath: str) -> tuple[np.ndarray, np.ndarray] | None:
    capture = cv2.VideoCapture(videoPath)
    if not capture.isOpened():
        print("Error: could not open video")
        exit(1)

    xPoints: np.ndarray = np.array([])
    yPoints: np.ndarray = np.array([])
    timeStamps: np.ndarray = np.array([])

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
        timeStamps = np.append(timeStamps, capture.get(cv2.CAP_PROP_POS_MSEC))
        
    capture.release()

    coords = np.vstack((xPoints, yPoints))

    return coords, timeStamps

def transformPoints(matrix, coords: np.ndarray):
    transformed = matrix @ coords
    return transformed


def getVideoFrame(videoPath: str, desiredFrameNum: int) -> np.ndarray:
    capture = cv2.VideoCapture(videoPath)
    if not capture.isOpened():
        print("Error: could not open video")
        exit(1)

    frameNum = 0

    while capture.isOpened():
        ret, frame = capture.read()

        if ret == False:
            print("Reached the end of the video or failed to load frame before desired frame")
            exit(1)

        if frameNum == desiredFrameNum:
            return frame

        frameNum += 1

    exit(1)
    

def loadImage(imagePath: str):
    return cv2.imread(imagePath)

if __name__ == "__main__":
    #centerX, centerY = findBallCenter("images/testImage.png")
    #print(f"Center coordinates found at: X={centerX}, Y={centerY}")

    #xPoints, yPoints = grapher.loadData(fileOutPath)

    #"""
    output = computeVideo(videoPath)

    if output == None:
        print("Video ran into an error")
        exit()

    coords, timeStamps = output

    grapher.writeData(fileOutPath, coords, timeStamps)

    grapher.graphPoints(timeStamps, coords[0])
    grapher.graphPoints(timeStamps, coords[1])
    #grapher.graphPoints(np.array([centerX]), np.array([centerY]))
    #"""




cv2.destroyAllWindows()