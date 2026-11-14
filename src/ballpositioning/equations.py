import numpy as np
from math import sqrt
from numpy.polynomial import Polynomial
from enum import Enum

class Line:
    # Coefficients are lowest degree to highest degree
    poly: Polynomial

    xPoints: np.ndarray
    yPoints: np.ndarray

    residuals: np.int32

    initDiff: float

    def __init__(self, poly: Polynomial, residuals: np.int32, xPoints: np.ndarray, yPoints: np.ndarray) -> None:
        self.poly = poly
        self.xPoints = xPoints
        self.yPoints = yPoints
        self.initDiff = self.getDiff()
        self.residuals = residuals

    @classmethod
    def fit(cls, xPoints, yPoints, deg=3):
        poly, data = Polynomial.fit(xPoints, yPoints, deg, full=True)
        residuals: np.int32 = data[0] # type: ignore
        return Line(poly, residuals, xPoints, yPoints)

    @classmethod
    def fit2(cls, poly: Polynomial, xPoints, yPoints):
        return Line(poly, calculateSSE(poly, xPoints, yPoints), xPoints, yPoints)

    def eval(self, minX, maxX):
        xLine = np.linspace(minX, maxX, 100)
        yLine = self.poly(xLine)
        return xLine, yLine

    def getDerivAtPoint(self, xPoint: float) -> float:
        deriv = self.poly.deriv()
        return deriv(xPoint)

    def getVelocityComponent(self, time: float) -> float:
        return self.getDerivAtPoint(time)

    def getDiff(self) -> float:
        yPredic = self.poly(self.xPoints)
        return np.mean((self.yPoints - yPredic))

    def deriv(self):
        return Line.fit2(self.poly.deriv(), self.xPoints, self.yPoints)

    def shiftX(self, distance):
        self.poly = self.poly(Polynomial([distance, 1]))

    def __str__(self) -> str:
        return f"{self.poly} R^2: {self.getDiff()}"

class TheoreticalLine(Line):
    def __init__(self, xPoints, yPoints, yStart0: bool=True, calcDegree=3):
        truePoly = Line.fit(xPoints, yPoints, calcDegree)
        initYVelocity = truePoly.getVelocityComponent(0)
        startY = yPoints[0] if yStart0 else 0
        poly = Polynomial([startY, initYVelocity, -9.8/2])
        SSE = calculateSSE(poly, xPoints, yPoints)
        super().__init__(poly, SSE, xPoints, yPoints)

def calculateSSE(poly: Polynomial, xPoints, yPoints):
    return np.sum((yPoints - poly(xPoints) ** 2))

def getVelocityAtPoint(yPoly: Line, xPoly: Line, time: float):
    dydt = yPoly.getDerivAtPoint(time)
    dxdt = xPoly.getDerivAtPoint(time)
    v0 = sqrt(dydt ** 2 + dxdt ** 2)
    return v0

# angle in radians
def getAngleAtPoint(yPoly: Line, xPoly: Line, time: float):
    dydt = yPoly.getDerivAtPoint(time)
    dxdt = xPoly.getDerivAtPoint(time)
    slope = dydt / dxdt
    return np.arctan(slope)

def getPercentError(predicted, actual):
    return abs((actual - predicted) / actual) * 100

class Point:
    x: float
    y: float
    z: float

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z