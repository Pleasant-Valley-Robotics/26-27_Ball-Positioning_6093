import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy import Symbol
from sympy.physics.units import degrees, radians, convert_to, meters, feet

startx, starty, startz, goalx, goaly, goalz = sp.symbols('startx starty startz goalx goaly goalz')
startx = 0
starty = 0
startz = 0
# goalx = 2.5
goaly = 2.5
# goalz = 0

maxX = 7 * feet # type: ignore
maxY = 5 * feet # type: ignore

thetay, thetax, v0 = sp.symbols('thetay thetax v0')
# thetay = 45 * degrees # type: ignore
# thetay = convert_to(thetay, radians)
thetay = 1.39626
# thetax = 0 * degrees # type: ignore

robotvx, robotvz = sp.symbols('robotvx robotvz')
# robotvx = 0
# robotvz = 0

g = sp.symbols("g")
g = -9.8

v0x, v0y, v0z = sp.symbols("v0x v0y v0z")

x = sp.symbols("x")

xA = v0x + robotvx
xB = startx

t = sp.symbols("t")
fx = xA*t + xB

fx_solutions = sp.solve(sp.Eq(fx, x), t)
ftx = fx_solutions[0]

z = sp.symbols("z")

zA = v0z + robotvz
zB = startz

fz = zA*t + zB

fz_solutions = sp.solve(sp.Eq(fz, z), t)
ftz = fz_solutions[0]

# print(ft)

yA = g/2
yB = v0y
yC = starty

fy = yA*t**2 + yB*t + yC

fxy = fy.subs(t, ftx)
fxz = fz.subs(t, ftx)

dfx = sp.diff(fx, t)
dfy = sp.diff(fy, t)
dfz = sp.diff(fz, t)

v0yPolar = v0 * sp.sin(thetay)
v0Horisontal = v0 * sp.cos(thetay)
v0xPolar = v0Horisontal * sp.cos(thetax)
v0zPolar = v0Horisontal * sp.sin(thetax)

expandedFy = fy.subs({v0y: v0yPolar})
expandedFz = fz.subs({v0z: v0zPolar})
expandedFx = fx.subs({v0x: v0xPolar})
finalTime = sp.solve(expandedFy - goaly, t)[1]
xEq = expandedFx.subs({t: finalTime}) - goalx
zEq = expandedFz.subs({t: finalTime}) - goalz
# sp.pprint(xEq)
# sp.pprint(zEq)
# solutions = sp.solve([finalTime, xEq, zEq], (thetax), dict=True)
# v0Solutions = sp.solve([finalTime.subs(solutions[0]), xEq.subs(solutions[0], zEq.subs(solutions[0]))], v0, dict=True)
thetaxValue = sp.solve([xEq, zEq], thetax, dict=True)[0]
# print(thetaxValue)
xEq2 = xEq.subs(thetaxValue)
zEq2 = zEq.subs(thetaxValue)
solutions = sp.solve([xEq2, zEq2], v0)
print(solutions)

# v0Actual = sp.solve(sp.Eq(eq1V0, eq2V0), thetax)
# print(v0Actual)
# sp.pprint(v0Actual)
# exit()
# print(eq2V0)
# exit()
# solutions = sp.solve([eq1V0, eq2V0], (v0, thetax))
# sp.pprint(solutions)
# sp.pprint(v0.simplify())