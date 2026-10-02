import matplotlib.pyplot as plt
import numpy as np


def graphPoints(xPoints: np.ndarray, yPoints: np.ndarray):
    plt.scatter(xPoints, yPoints)
    plt.show()

def loadData(filePath: str):
    xPoints: np.ndarray = np.array([])
    yPoints: np.ndarray = np.array([])
    timeStamps: np.ndarray = np.array([])
    with open(filePath, "r") as file:
        for line in file:
            data = line.strip()
            data = data.split(" ")
            if len(data) == 2:
                xPoints = np.append(xPoints, data[0])
                yPoints = np.append(yPoints, data[1])
                timeStamps = np.append(timeStamps, data[2])


    coords = np.vstack((xPoints, yPoints))

    return coords, timeStamps

def writeData(filePath: str, coords: np.ndarray, timeStamps: np.ndarray):
    xPoints = coords[0]
    yPoints = coords[1]
    with open(filePath, "w") as file:
        for x, y, z in zip(xPoints, yPoints, timeStamps):
            file.write(f"{x} {y} {z}\n")

if __name__ == "__main__":
    coords, timeStamps = loadData("data.txt")
    graphPoints(coords[0], coords[1])