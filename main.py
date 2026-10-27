from src.visualWidget import PointGrabber
from src.visualWidget import FrameGrabber
import src.converter as converter
import src.grapher as grapher

filePrefix = "trial"
startNum = 1
endNum = 7

outputFolder = "DIO_FIRST_1000_Trials"

def runVideo(fileName: str):
    pointGrabber = PointGrabber()
    pointGrabber.setFileName(fileName)
    videoPath = converter.getVideoPath(fileName)
    pointGrabber.openWindow()
    pointGrabber.loadVideo(10)
    points = pointGrabber.getPoints(2)
    pointGrabber.closeWindow()

    frameGrabber = FrameGrabber()
    frameGrabber.setFileName(fileName)
    startFrame = frameGrabber.getFrame(0)
    endFrame = frameGrabber.getFrame(startFrame)

    print(startFrame, endFrame)

    if points is None:
        print("Could not grab points")
        exit(1)

    dimensions = converter.getVideoDimensions(videoPath)
    if dimensions is None:
        print("Could not open video")
        exit(1)

    computeOutput = converter.computeVideo(videoPath, startFrame, endFrame)
    if computeOutput is None:
        print("There was an error in computing video")
        exit(1)
    coords, timeStamps = computeOutput
    matrix = converter.get2PTransformMatrix(points[0], points[1], dimensions)

    realPoints = converter.transformPoints(matrix, coords)

    grapher.graphPoints(timeStamps, realPoints[0], "Time (s)", "X (m)")
    grapher.graphPoints(timeStamps, realPoints[1], "Time (s)", "Y (m)")

    grapher.writeData(f"{outputFolder}/{fileName}", realPoints, timeStamps)


#for trialNum in range(startNum, endNum+1):
#    runVideo(f"{filePrefix}{trialNum}")

#runVideo("PositionExam")
grapher.testMultiple()
# grapher.testSingle()