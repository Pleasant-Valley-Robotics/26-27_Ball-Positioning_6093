import numpy as np
from math import sqrt
from numpy.polynomial import Polynomial

# Coefficients are lowest degree to highest degree
def getPoly(xPoints, yPoints, deg) -> Polynomial:
    poly = Polynomial.fit(xPoints, yPoints, deg)
    return poly

def evalPoly(poly: Polynomial, minX, maxX):
    xLine = np.linspace(minX, maxX, 100)
    yLine = poly(xLine)
    return xLine, yLine

def printPoly(poly: Polynomial):
    print(poly)

def xShiftPoly(poly: Polynomial, distance):
    #shifted = poly.convert(domain=poly.domain + distance, window=poly.window)
    shifted = poly(Polynomial([distance, 1]))
    return shifted

def getDirivAtPoint(poly: Polynomial, xPoint: float):
    deriv = poly.deriv()
    return deriv(xPoint)

def getVelocityAtPoint(yPoly: Polynomial, xPoly: Polynomial, time: float):
    dydt = getDirivAtPoint(yPoly, time) * 1000 * 8
    dxdt = getDirivAtPoint(xPoly, time) * 1000 * 8
    v0 = sqrt(dydt ** 2 + dxdt ** 2)
    return v0

# angle in radians
def getAngleAtPoint(yPoly: Polynomial, xPoly: Polynomial, time: float):
    dydt = getDirivAtPoint(yPoly, time)
    dxdt = getDirivAtPoint(xPoly, time)
    slope = dydt / dxdt
    return np.arctan(slope)