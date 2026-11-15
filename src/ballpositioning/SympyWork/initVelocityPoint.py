import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy import Symbol

from ballpositioning.equations import Point

startx, starty, goalx, goaly = sp.symbols('startx starty goalx goaly')
# startx = 0
# starty = 0
# goalx = 2.5
# goaly = 2.5

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

finalTime = ft.subs({x: goalx})
# print(finalTime)
netVelocity = sp.sqrt(sp.sympify(dfx**2) + sp.sympify(dfy**2))
# netFinalVelocities = sp.solve(netVelocity.simplify() - finalTime, t)
netFinalVelocities = netVelocity.subs({t: finalTime})
# print(netFinalVelocities)
netFinalVelocity = netFinalVelocities
v0yRelation = sp.solve(fxy.subs({x: goalx}) - goaly, (v0x, v0y), dict=True)[0]
sp.pprint(v0yRelation)
finalVelocity = netFinalVelocity.subs(v0yRelation)

# bestv0x = sp.solve(finalVelocity)

sp.pprint(finalVelocity.simplify())
f = sp.lambdify([v0x], finalVelocity.subs({startx: 0, starty: 0, goalx: 2.5, goaly: 2.5}))

xValues = np.linspace(0, 20, 200)
yValues = f(xValues)

plt.rcParams['axes3d.mouserotationstyle'] = 'azel'
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)

ax.plot(xValues, yValues)

ax.set_xlabel('Initial X Velocity')
ax.set_ylabel('Ending Net Velocity')
ax.set_title('Net Velocity at Final Position Given Initial X Velocity')

plt.show()