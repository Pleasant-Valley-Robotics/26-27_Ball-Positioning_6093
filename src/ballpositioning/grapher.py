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

def getEquations(coords, timeStamps) -> tuple[Polynomial, Polynomial]:
    xPoly = getPoly(timeStamps, coords[0], 1)
    yPoly = getPoly(timeStamps, coords[1], 2)
    xPoly -= xPoly(0)
    yPoly -= yPoly(0)
    return xPoly, yPoly

def graphFile(filePath: str):
    coords, timeStamps = loadData(filePath)
    graphPoints(timeStamps, coords[1], "Time", "Y Position")
    graphPoints(timeStamps, coords[0], "Time", "X Position")

def testSingle():
    coords, timeStamps = loadData("data/transformed/MultiCompute_2/1300_MotorSpeed/20261027_191051.txt")
    plt.title("X Position vs Time at 1300 Motor Speed.")
    fitGraph(timeStamps, coords[1], "Time (s)", "X (m)", 2)

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

def testFolder(folderPath: Path):
    coeffs = []
    V0s = []
    thetas = []
    for file in folderPath.rglob("*"):
        coords, timeStamps = loadData(str(file))
        xPoly, yPoly = getEquations(coords, timeStamps)
        yVel = yPoly.deriv()
        yAcc = yVel.deriv()
        xVel = xPoly.deriv()
        V0s.append(getVelocityAtPoint(yPoly, xPoly, 0))
        thetas.append(np.degrees(getAngleAtPoint(yPoly, xPoly, 0)))
        # xLine, yLine = evalPoly(yPoly, 0, max(timeStamps))
        # addLine(xLine, yLine)
        coeffs.append(yPoly.coef[2])
        
    plt.hist(thetas, 30, density=True)
    # plt.xlabel("Time (s)")
    # plt.ylabel("Y Position (m)")
    # plt.title("DIO Ball paths at some motor speed idk")
    plt.show()

if __name__ == "__main__":
    # testMultiple()
    testSingle()
    # graphFile("data/legacy/data.txt")
    # testFolder(Path("data/transformed/MultiCompute_2/1300_MotorSpeed"))