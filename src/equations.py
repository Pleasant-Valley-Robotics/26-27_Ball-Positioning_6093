import numpy as np
from math import sqrt
from numpy.polynomial import Polynomial

def getPoly(xPoints, yPoints, deg):
    coeff = np.polyfit(xPoints, yPoints, deg)
    return list(coeff)

def evalPoly(coeff, minX, maxX):
    xLine = np.linspace(minX, maxX, 100)
    yLine = np.polyval(coeff, xLine)
    return xLine, yLine

def printPoly(coeff):
    poly = Polynomial(coeff[::-1])
    print(poly)

# Coeff are high to low
def xShiftPoly(coeff, distance):
    originalPoly = Polynomial(coeff[::-1])
    shiftedPoly = originalPoly.convert(domain=originalPoly.domain + distance, window=originalPoly.window)
    return list(shiftedPoly.coef[::-1])
    
def getDirivAtPoint(coeff, xPoint):
    poly = Polynomial(coeff[::-1])
    deriv = poly.deriv()
    return deriv(xPoint)

def getVelocityAtPoint(yCoeff, xCoeff, time):
    dydt = getDirivAtPoint(yCoeff, time) * 1000 * 8
    dxdt = getDirivAtPoint(xCoeff, time) * 1000 * 8
    v0 = sqrt(dydt ** 2 + dxdt ** 2)
    return v0

# angle in radians
def getAngleAtPoint(yCoeff, xCoeff, time):
    dydt = getDirivAtPoint(yCoeff, time)
    dxdt = getDirivAtPoint(xCoeff, time)
    slope = dydt / dxdt
    return np.arctan(slope)