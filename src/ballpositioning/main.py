from ballpositioning.visualWidget import PointGrabber
from ballpositioning.visualWidget import FrameGrabber
import ballpositioning.converter as converter
import ballpositioning.grapher as grapher
import ballpositioning.fileIO as fileIO

from pathlib import Path

from tqdm import tqdm

def runVideo(filePath: Path):
    pointGrabber = PointGrabber()
    pointGrabber.setFileName(filePath)
    pointGrabber.openWindow()
    pointGrabber.loadVideo(10)
    points = pointGrabber.getPoints(3)
    pointGrabber.closeWindow()

    frameGrabber = FrameGrabber()
    frameGrabber.setFileName(filePath)
    startFrame = frameGrabber.getFrame(0)
    endFrame = frameGrabber.getFrame(startFrame)

    # print(startFrame, endFrame)

    if points is None:
        print("Could not grab points")
        return

    dimensions = converter.getVideoDimensions(filePath)
    if dimensions is None:
        print("Could not open video")
        return

    computeOutput = converter.computeVideo(filePath, startFrame, endFrame)
    if computeOutput is None:
        print("There was an error in computing video")
        return
    coords, timeStamps = computeOutput

    outputFolder: Path = (filePath.relative_to(Path("videos"))).with_suffix("")

    fileIO.writeData("raw" / outputFolder, coords, timeStamps, [points[0], points[1], points[2]])

    matrix = converter.get2PTransformMatrix(points[0], points[1], dimensions)

    realPoints, correctedTime = converter.transformPoints(matrix, coords, timeStamps)

    fileIO.writeData("transformed" / outputFolder, realPoints, correctedTime)

    # grapher.graphPoints(timeStamps, realPoints[0], "Time (s)", "X (m)")
    # grapher.graphPoints(timeStamps, realPoints[1], "Time (s)", "Y (m)")


directory = Path("videos/MultiCompute_2")


for path in tqdm(directory.rglob("*")):
    if path.is_file():
        runVideo(path)
        # exit()

# grapher.testMultiple()
# grapher.testSingle()
# grapher.graphFile("data/transformed/MultiCompute_2/1500_MotorSpeed_1/20261027_190232.txt")
