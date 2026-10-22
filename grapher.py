import matplotlib.pyplot as plt
import numpy as np


def graphPoints(xPoints: np.ndarray, yPoints: np.ndarray, xLabel: str = "", yLabel: str = ""):
    plt.scatter(xPoints, yPoints)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    #yMin = yPoints.min()
    #yMax = yPoints.max()
    #plt.ylim(yMin, yMax)
    plt.show()

def fitGraph(xPoints: np.ndarray, yPoints: np.ndarray, xLabel: str="", yLabel: str=""):
    #a, b, c, d = np.polyfit(xPoints, yPoints, deg=3)
    #x_line = np.linspace(min(xPoints), max(xPoints), 100)
    ##y_line = b * x_line**2 + c * x_line + d
    #y_line = a * x_line**3 + b * x_line**2 + c * x_line + d
    ##equation_text = f"y = {b:.10f}x^2 + {c:.5f}x + {d:.5f}"
    #equation_text = f"y = {a:.10f}x^3 + {b:.10f}x^2 + {c:.5f}x + {d:.5f}"
    #print(equation_text)
    coeff = list(getPoly(xPoints, yPoints))
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

# Coeff are high to low
def xShiftPoly(coeff, distance):
    originalPoly = np.polynomial.Polynomial(coeff[::-1])
    shiftedPoly = originalPoly.convert(domain=originalPoly.domain + distance, window=originalPoly.window)
    return list(shiftedPoly.coef[::-1])

def getPoly(xPoints, yPoints, deg=3):
    coeff = np.polyfit(xPoints, yPoints, deg)
    return list(coeff)

def evalPoly(coeff, minX, maxX):
    xLine = np.linspace(minX, maxX, 100)
    yLine = np.polyval(coeff, xLine)
    return xLine, yLine

def loadData(filePath: str):
    xPoints: np.ndarray = np.array([])
    yPoints: np.ndarray = np.array([])
    timeStamps: np.ndarray = np.array([])
    with open(filePath, "r") as file:
        for line in file:
            data = line.strip()
            data = data.split(" ")
            if len(data) == 3:
                xPoints = np.append(xPoints, float(data[0]))
                yPoints = np.append(yPoints, float(data[1]))
                timeStamps = np.append(timeStamps, float(data[2]))


    coords = np.vstack((xPoints, yPoints))

    return coords, timeStamps



def writeData(filePath: str, coords: np.ndarray, timeStamps: np.ndarray):
    xPoints = coords[0]
    yPoints = coords[1]
    with open("data/" + filePath + ".txt", "w") as file:
        for x, y, z in zip(xPoints, yPoints, timeStamps):
            file.write(f"{x} {y} {z}\n")

def addLine(xPoints, yPoints):
    plt.plot(
        xPoints,
        yPoints,
        #linestyle="--",
        linewidth=3,
    )

def getVelocityAtPoint(coeff, xPoint):
    p = np.polynomial.Polynomial(coeff[::-1])
    pDeriv = p.deriv()
    return pDeriv(xPoint) * 1000 * 8

# angle in radians
def getAngleAtPoint(coeff, xPoint):
    slope = getVelocityAtPoint(coeff, xPoint)
    return np.arctan(slope)

def addWrongLineData(coords, timeStamps):
    startingHeight = .42803907627239823
    correctedTime = timeStamps - timeStamps[0]
    coeff = getPoly(correctedTime, coords[1], 3)
    roots = np.roots(coeff[:-1] + [coeff[-1] - startingHeight])
    startX = roots[-1]
    coeff = xShiftPoly(coeff, startX)
    print(getVelocityAtPoint(coeff, 0))
    print(np.degrees(getAngleAtPoint(coeff, 0)))
    xLine, yLine = evalPoly(coeff, 0, max(correctedTime))
    addLine(xLine, yLine)


def testSingle():
    coords, timeStamps = loadData("data/trial1.txt")
    fitGraph(timeStamps, coords[1], "Time (ms)", "Y (m)")

def testMultiple():
    coords1, timeStamps1 = loadData("data/trial1.txt")
    coords2, timeStamps2 = loadData("data/trial2.txt")
    coords3, timeStamps3 = loadData("data/trial3.txt")
    coords4, timeStamps4 = loadData("data/trial4.txt")
    coords5, timeStamps5 = loadData("data/trial5.txt")
    coords6, timeStamps6 = loadData("data/trial6.txt")
    coords7, timeStamps7 = loadData("data/trial7.txt")
    addWrongLineData(coords1, timeStamps1)
    addWrongLineData(coords2, timeStamps2)
    addWrongLineData(coords3, timeStamps3)
    addWrongLineData(coords4, timeStamps4)
    addWrongLineData(coords5, timeStamps5)
    addWrongLineData(coords6, timeStamps6)
    addWrongLineData(coords7, timeStamps7)
    plt.xlabel("Time (ms)")
    plt.ylabel("Y Position (m)")
    plt.title("DIO Ball paths at 1000 motor speed")
    plt.show()

if __name__ == "__main__":
    testMultiple()
    #testSingle()