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
    x_line, y_line = getXYEquation(xPoints, yPoints)

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
    a, b, c, d = coeff
    originalPoly = np.polynomial.Polynomial([d, c, b, a])
    shiftedPoly = originalPoly.convert(domain=originalPoly.domain + distance, window=originalPoly.window)
    d2, c2, b2, a2 = shiftedPoly.coef
    return [a2, b2, c2, d2]

def getPoly(xPoints, yPoints):
    coeff = np.polyfit(xPoints, yPoints, deg=3)
    return coeff

def getXYEquation(xPoints, yPoints):
    a, b, c, d = np.polyfit(xPoints - xPoints[0], yPoints, deg=3)
    minX = np.roots([a, b, c, d - .42803907627239823])
    coeff = xShiftPoly([a, b, c, d], minX[2])
    xLine = np.linspace(0, max(xPoints - xPoints[0]))
    yLine = np.polyval(coeff, xLine)
    #yLine = a2 * xLine**3 + b2 * xLine**2 + c2 * xLine + d2
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

def addGraph(coords, timeStamps):
    plt.scatter(timeStamps - timeStamps[0], coords[1])
    #for coords, timeStamps in zip(coordss, timeStampss):
    #    plt.scatter(coords, timeStamps)

def addLine(xPoints, yPoints):
    plt.plot(
        xPoints,
        yPoints,
        #linestyle="--",
        linewidth=3,
    )

def addLineData(coords, timeStamps):
    xLine, yLine = getXYEquation(timeStamps, coords[1])
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
    addLineData(coords1, timeStamps1)
    addLineData(coords2, timeStamps2)
    addLineData(coords3, timeStamps3)
    addLineData(coords4, timeStamps4)
    addLineData(coords5, timeStamps5)
    addLineData(coords6, timeStamps6)
    addLineData(coords7, timeStamps7)
    plt.xlabel("Time (ms)")
    plt.ylabel("Y Position (m)")
    plt.title("DIO Ball paths at 1000 motor speed")
    plt.show()

if __name__ == "__main__":
    testMultiple()
    #testSingle()