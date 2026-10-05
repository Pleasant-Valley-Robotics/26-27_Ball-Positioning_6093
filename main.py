import visualWidget
import converter
import grapher

fileName = "fullTest.mp4"

output = "data1.txt"

grabber = visualWidget.PointGrabber()
grabber.setImageName(fileName)
grabber.openWindow()
grabber.loadImage(10)
points = grabber.getPoints(2)
grabber.closeWindow()

if points is None:
    print("Could not grab points")
    exit(1)

computeOutput = converter.computeVideo(converter.getVideoPath(fileName))
if computeOutput is None:
    print("There was an error in computing video")
    exit(1)
coords, timeStamps = computeOutput
matrix = converter.get2PTransformMatrix(points[0], points[1])

realPoints = converter.transformPoints(matrix, coords)

grapher.graphPoints(timeStamps, realPoints[0])
grapher.graphPoints(timeStamps, realPoints[1])

grapher.writeData(output, realPoints, timeStamps)