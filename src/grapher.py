import matplotlib.pyplot as plt
import numpy as np

from src.fileIO import *
from src.equations import *

def graphPoints(xPoints: np.ndarray, yPoints: np.ndarray, xLabel: str = "", yLabel: str = ""):
    plt.scatter(xPoints, yPoints)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    #yMin = yPoints.min()
    #yMax = yPoints.max()
    #plt.ylim(yMin, yMax)
    plt.show()

def fitGraph(xPoints: np.ndarray, yPoints: np.ndarray, xLabel: str="", yLabel: str="", degree: int =3):
    coeff = list(getPoly(xPoints, yPoints, degree))
    x_line, y_line = evalPoly(coeff, min(xPoints), max(xPoints))

    plt.scatter(xPoints, yPoints)

    plt.plot(
        x_line,
        y_line,
        color="red",
        linestyle="--",
        linewidth=3,
    )

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()


def addLine(xPoints, yPoints):
    plt.plot(
        xPoints,
        yPoints,
        #linestyle="--",
        linewidth=3,
    )

def addWrongLineData(coords, timeStamps) -> None:
    startingHeight = .42803907627239823
    correctedTime = timeStamps - timeStamps[0]
    yCoeff = getPoly(correctedTime, coords[1], 3)
    roots = np.roots(yCoeff[:-1] + [yCoeff[-1] - startingHeight])
    startX = roots[-1]
    yCoeff = xShiftPoly(yCoeff, startX)
    xCoeff = getPoly(correctedTime, coords[0], 1)
    xCoeff = xShiftPoly(xCoeff, startX)
    print(getVelocityAtPoint(yCoeff, xCoeff, 0))
    print(np.degrees(getAngleAtPoint(yCoeff, xCoeff, 0)))
    # printPoly(yCoeff)
    xLine, yLine = evalPoly(yCoeff, 0, max(correctedTime))
    addLine(xLine, yLine)

def graphFile(filePath: str):
    coords, timeStamps = loadData("data/" + filePath)
    graphPoints(timeStamps, coords[1], "Time", "Y Position")
    graphPoints(timeStamps, coords[0], "Time", "X Position")

def testSingle():
    coords, timeStamps = loadData("data/trial1.txt")
    fitGraph(timeStamps, coords[1], "Time (ms)", "Y (m)")

def testMultiple():
    startNum = 1
    endNum = 7
    for trialNum in range(startNum, endNum + 1):
        if trialNum in [1, 3, 6]:
            continue
            pass
        coords, timeStamps = loadData(f"data/trial{trialNum}.txt")
        addWrongLineData(coords, timeStamps)
    plt.xlabel("Time (ms)")
    plt.ylabel("Y Position (m)")
    plt.title("DIO Ball paths at 1000 motor speed")
    plt.show()

if __name__ == "__main__":
    testMultiple()
    #testSingle()
    #graphFile("legacy/data.txt")