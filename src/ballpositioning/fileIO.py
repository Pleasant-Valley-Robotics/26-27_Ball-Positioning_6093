import numpy as np

def writeData(filePath: str, coords: np.ndarray, timeStamps: np.ndarray):
    xPoints = coords[0]
    yPoints = coords[1]
    with open("data/" + filePath + ".txt", "w") as file:
        for x, y, z in zip(xPoints, yPoints, timeStamps):
            file.write(f"{x} {y} {z}\n")
            
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