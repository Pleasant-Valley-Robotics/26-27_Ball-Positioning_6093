import matplotlib.pyplot as plt
import numpy as np

from ballpositioning.fileIO import *
from ballpositioning.equations import *

def graphPoints(xPoints: np.ndarray, yPoints: np.ndarray, xLabel: str = "", yLabel: str = ""):
    plt.scatter(xPoints, yPoints)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    #yMin = yPoints.min()
    #yMax = yPoints.max()
    #plt.ylim(yMin, yMax)
    plt.show()

def fitGraph(xPoints: np.ndarray, yPoints: np.ndarray, xLabel: str="", yLabel: str="", degree: int =3):
    coeff = getPoly(xPoints, yPoints, degree)
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

def getWrongEquations(coords, timeStamps) -> tuple[Polynomial, Polynomial]:
    startingHeight = .42803907627239823
    correctedTime = timeStamps - timeStamps[0]
    yPoly = getPoly(correctedTime, coords[1], 3)
    roots = (yPoly - startingHeight).roots()
    startX = roots[0]
    yPoly = xShiftPoly(yPoly, startX)
    xPoly = getPoly(correctedTime, coords[0], 1)
    xPoly = xShiftPoly(xPoly, startX)
    return xPoly, yPoly

def graphFile(filePath: str):
    coords, timeStamps = loadData("data/" + filePath)
    graphPoints(timeStamps, coords[1], "Time", "Y Position")
    graphPoints(timeStamps, coords[0], "Time", "X Position")

def testSingle():
    coords, timeStamps = loadData("data/PositionExam.txt")
    plt.title("X Position vs Time at 1000 Motor Speed.")
    fitGraph(timeStamps, coords[0], "Time (ms)", "X (m)", 1)

def testMultiple():
    startNum = 1
    endNum = 7
    for trialNum in range(startNum, endNum + 1):
        if trialNum in [1, 3, 6]:
            # continue
            pass
        coords, timeStamps = loadData(f"data/DIO_first_1000_Trials/trial{trialNum}.txt")
        xPoly, yPoly = getWrongEquations(coords, timeStamps)
        xLine, yLine = evalPoly(yPoly, 0, max(timeStamps - timeStamps[0]))
        addLine(xLine, yLine)
        # print(getVelocityAtPoint(yPoly, xPoly, 0))
        # print(np.degrees(getAngleAtPoint(yPoly, xPoly, 0)))
    
    plt.xlabel("Time (ms)")
    plt.ylabel("Y Position (m)")
    plt.title("DIO Ball paths at 1000 motor speed")
    plt.show()

if __name__ == "__main__":
    testMultiple()
    #testSingle()
    #graphFile("legacy/data.txt")