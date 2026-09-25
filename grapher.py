import matplotlib.pyplot as plt
import numpy as np


def graphPoints(xPoints, yPoints):
    plt.scatter(xPoints, yPoints)
    plt.show()

def loadData(filePath: str):
    xPoints: np.ndarray = np.array([])
    yPoints: np.ndarray = np.array([])
    with open(filePath, "r") as file:
        for line in file:
            data = line.strip()
            data = data.split(" ")
            if len(data) == 2:
                xPoints = np.append(xPoints, data[0])
                yPoints = np.append(yPoints, data[1])


    return xPoints, yPoints

def writeData(filePath: str, xPoints: np.ndarray, yPoints: np.ndarray):
    with open(filePath, "w") as file:
        for x, y in zip(xPoints, yPoints):
            file.write(f"{x} {y}\n")

if __name__ == "__main__":
    xPoints, yPoints = loadData("data.txt")
    graphPoints(xPoints, yPoints)