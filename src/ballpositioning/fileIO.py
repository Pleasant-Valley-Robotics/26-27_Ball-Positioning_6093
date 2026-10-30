import numpy as np
from pathlib import Path

def writeData(filePath: Path, coords: np.ndarray, timeStamps: np.ndarray, headerData: list|None=None):
    header = ""
    if headerData is not None:
        # print(str(" ".join(headerData[0])))
        header = ", ".join([" ".join([str(value) for value in point]) for point in headerData])
    xPoints = coords[0]
    yPoints = coords[1]
    path = "data" / filePath.with_suffix(".txt")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as file:
        file.write(header)
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