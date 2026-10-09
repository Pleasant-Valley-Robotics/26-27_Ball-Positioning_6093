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
    a, b, c, d = np.polyfit(xPoints, yPoints, deg=3)
    x_line = np.linspace(min(xPoints), max(xPoints), 100)
    y_line = a * x_line**3 + b * x_line**2 + c * x_line + d
    equation_text = f"y = {a:.10f}x^3 + {b:.10f}x^2 + {c:.5f}x + {d:.5f}"
    print(equation_text)

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

if __name__ == "__main__":
    coords, timeStamps = loadData("data1.txt")
    fitGraph(timeStamps, coords[1], "Time (s)", "Y (m)")

    #graphPoints(timeStamps, coords[0], "Time (s)", "X (m)")
    #graphPoints(timeStamps, coords[1], "Time (s)", "Y (m)")