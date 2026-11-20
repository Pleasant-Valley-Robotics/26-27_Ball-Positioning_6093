import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy import Symbol
from sympy.physics.units import degrees, radians, convert_to, meters, feet

startx, starty, goalx, goaly = sp.symbols('startx starty goalx goaly')
startx = 0
starty = 0
# goalx = 2.5
# goaly = 2.5

maxX = 7 * feet # type: ignore
maxY = 5 * feet # type: ignore

theta, v0 = sp.symbols('theta v0')
# theta = 45 * degrees # type: ignore

g = sp.symbols("g")
g = -9.8

v0x, v0y = sp.symbols("v0x v0y")

x = sp.symbols("x")

xA = v0x
xB = startx

t = sp.symbols("t")
fx = xA*t + xB

fx_solutions = sp.solve(sp.Eq(fx, x), t)
ft = fx_solutions[0]

# print(ft)

yA = g/2
yB = v0y
yC = starty

fy = yA*t**2 + yB*t + yC

fxy = fy.subs(t, ft)

dfx = sp.diff(fx, t)
dfy = sp.diff(fy, t)

# v0yRelation = sp.solve(fxy.subs(x, goalx) - goaly, (v0x, v0y), dict=True)[0]
# v0yRelation2 = v0x * sp.tan(theta)
# v0xValue = sp.solve(sp.Eq(v0yRelation[v0y], v0yRelation2), v0x)[1]
# v0yValue = v0yRelation[v0y].subs(v0x, v0xValue)
# v0 = sp.sqrt(v0xValue ** 2 + v0yValue ** 2)
# sp.pprint(v0yValue.simplify())

fullEq = fxy.subs({v0x: v0 * sp.cos(theta), v0y: v0 * sp.sin(theta)})
v0 = sp.solve(fullEq.subs(x, goalx) - goaly, v0)[1]
sp.pprint(v0.simplify())