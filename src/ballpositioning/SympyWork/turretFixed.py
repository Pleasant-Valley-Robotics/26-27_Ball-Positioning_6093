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
# goalz = 2.5

maxX = 7 * feet # type: ignore
maxY = 5 * feet # type: ignore

thetay, thetax, v0 = sp.symbols('thetay thetax v0')
thetay = 45 * degrees # type: ignore

robotvx, robotvz = sp.symbols('robotvx robotvz')
# robotvx = 1
# robotvz = 1

g = sp.symbols("g")
g = -9.8

v0x, v0y, v0z = sp.symbols("v0x v0y v0z")

x = sp.symbols("x")

xA = v0x + robotvz
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
v0xPolar = v0Horisontal * sp.sin(thetax)
v0zPolar = v0Horisontal * sp.cos(thetax)

expandedFxy = fxy.subs({v0x: v0xPolar, v0y: v0yPolar})
expandedFxz = fxz.subs({v0x: v0xPolar, v0z: v0zPolar})
eq1 = expandedFxy.subs(x, goalx) - goaly
# eq1V0 = sp.solve(eq1, v0)[0].simplify()
eq2 = expandedFxz.subs(x, goalx) - goalz
# eq2V0 = sp.solve(eq2, v0)[0].simplify()
# v0Actual = sp.solve(sp.Eq(eq1V0, eq2V0), thetax)
# print(v0Actual)
# sp.pprint(v0Actual)
# exit()
# print(eq2V0)
# exit()
solutions = sp.solve([eq1.simplify(), eq2.simplify()], (v0, thetax))
print(solutions)
# sp.pprint(v0.simplify())