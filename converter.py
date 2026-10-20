import cv2
import numpy as np
from pathlib import Path
from colorsys import hls_to_rgb

import grapher

blur = 11

lowerYellow = np.array([20, 100, 100])
upperYellow = np.array([30, 255, 255])

lowerGreenHSL = np.array([150, 20, 30]) # in hsl
upperGreenHSL = np.array([180, 100, 100]) # in hsl

lowerGreenHSV = np.array([150 - 20, 0, 92])
upperGreenHSV = np.array([179, 85 + 10, 100])

lowerGreen = np.array([70, 0, 150]) # idk why this works
upperGreen = np.array([90, 255, 255]) # idk man

"""
def hsl_to_hsv_pixel(h, s, l):
  r, g, b = hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
  # Convert RGB [0, 1] to BGR [0, 255] for OpenCV
  bgr_pixel = np.uint8([[[b * 255, g * 255, r * 255]]])
  # Convert BGR to OpenCV HSV (H: 0-179, S: 0-255, V: 0-255)
  hsv_pixel = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2HSV)
  return hsv_pixel[0][0]
"""

lower = lowerGreen
upper = upperGreen

def getVideoPath(fileName: str):
    return Path("videos") / (fileName + ".mp4")

def findBallCenter(image) -> tuple[int, int] | None:
    if image is None:
        print("Error: Image could not be read.")
        return None

    blurred = cv2.GaussianBlur(image, (blur, blur), 0)

    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
        
    moments = cv2.moments(mask)

    if moments["m00"] != 0:
        centerX = int(moments["m10"] / moments["m00"])
        centerY = int(moments["m01"] / moments["m00"])

        #cv2.circle(image, (centerX, centerY), 10, (0, 0, 255), -1)
        #cv2.imwrite("detected_center.png", image)

        return centerX, centerY
    
def get2PTransformMatrix(p1, p2, dimensions: tuple[int, int]):
    pixelDist = np.linalg.norm(p2 - p1)
    realDist = 1
    
    scale = realDist / pixelDist

    #averageY = (p1[1] + p2[1]) / 2
    averageY = dimensions[1] / scale

    M = np.array([
        [-scale, 0, dimensions[0]*scale],
        [0, -scale, dimensions[1]*scale - (averageY * scale - dimensions[1])],
        [0, 0, 1]
    ], dtype=np.float32)
    
    return M

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


def computeVideo(videoPath: Path, startFrame: int = 0, endFrame: float = float('inf')) -> tuple[np.ndarray, np.ndarray] | None:
    capture = cv2.VideoCapture(str(videoPath.resolve()))
    if not capture.isOpened():
        print("Error: could not open video")
        exit(1)

    xPoints: np.ndarray = np.array([])
    yPoints: np.ndarray = np.array([])
    timeStamps: np.ndarray = np.array([])

    capture.set(cv2.CAP_PROP_POS_FRAMES, startFrame)

    currentFrame: int = startFrame

    while capture.isOpened():
        ret, frame = capture.read()

        if ret == False or currentFrame > endFrame:
            print("Reached the end of the video or failed to load frame.")
            break

        position = findBallCenter(frame)

        if position is None:
            print("Can't find position of ball!")
            continue

        xPoints = np.append(xPoints, position[0])
        yPoints = np.append(yPoints, position[1])
        timeStamps = np.append(timeStamps, capture.get(cv2.CAP_PROP_POS_MSEC))

        currentFrame += 1
        
    capture.release()

    coords = np.vstack((xPoints, yPoints))

    timeStamps = timeStamps - timeStamps[0]
    timeStamps = timeStamps / (8 * 1000)

    return coords, timeStamps

def getVideoDimensions(videoPath: Path) -> tuple[int, int] | None:
    cap = cv2.VideoCapture(str(videoPath.resolve()))

    if not cap.isOpened():
        print("Error: Could not open video.")
        cap.release()
        return None
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cap.release()

    return width, height

def transformPoints(matrix, coords: np.ndarray):
    ones = np.ones((1, coords.shape[1]))
    new = np.vstack([coords, ones])
    transformed = matrix @ new
    transformed_2d = transformed[:2, :] / transformed[2, :]
    return transformed_2d


def getVideoFrame(videoPath: Path, desiredFrameNum: int) -> np.ndarray:
    capture = cv2.VideoCapture(str(videoPath.resolve()))
    if not capture.isOpened():
        print("Error: could not open video")
        exit(1)

    frameNum = 0

    capture.set(cv2.CAP_PROP_POS_FRAMES, desiredFrameNum)

    ret, frame = capture.read()
    if not ret:
        print("Reached the end of the video or failed to load frame before desired frame")
        exit(1)

    return frame

def loadImage(imagePath: str):
    return cv2.imread(imagePath)

if __name__ == "__main__":
    #videoPath = Path("videos/fullTest.mp4")

    #fileOutPath = "data.txt"
    
    #centerX, centerY = findBallCenter("images/testImage.png")
    #print(f"Center coordinates found at: X={centerX}, Y={centerY}")

    #xPoints, yPoints = grapher.loadData(fileOutPath)

    """
    output = computeVideo(videoPath)

    if output is None:
        print("Video ran into an error")
        exit()

    coords, timeStamps = output

    grapher.writeData(fileOutPath, coords, timeStamps)

    grapher.graphPoints(timeStamps, coords[0])
    grapher.graphPoints(timeStamps, coords[1])
    #grapher.graphPoints(np.array([centerX]), np.array([centerY]))
    """
    testImage = loadImage("images/greenTest.png")
    coords = findBallCenter(testImage)
    print(coords)


    cv2.destroyAllWindows()