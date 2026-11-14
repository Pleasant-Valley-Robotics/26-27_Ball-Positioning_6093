import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy import Symbol

from ballpositioning.equations import Point

startx, starty, minGoalx, minGoaly, maxGoalx, maxGoaly = sp.symbols('startx starty minGoalx minGoaly maxGoalx maxGoaly')
# startx = 0
# starty = 0
# minGoalx = 2
# minGoaly = 2
# maxGoalx = 3
# maxGoaly = 3

g = sp.symbols("g")
# g = -9.8

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

goalSlope = (maxGoaly - minGoaly) / (maxGoalx - minGoalx)
goalLine = minGoaly + goalSlope * (x - minGoalx)
finalX = sp.solve(goalLine - fxy, x)[1]
# print(finalX)

finalTime = ft.subs({x: finalX})
# print(finalTime)
netVelocity = sp.sqrt(sp.sympify(dfx**2) + sp.sympify(dfy**2))
# netFinalVelocities = sp.solve(netVelocity.simplify() - finalTime, t)
netFinalVelocities = netVelocity.subs({t: finalTime})
# print(netFinalVelocities)
netFinalVelocity = netFinalVelocities
intersectsGoal_min = fxy.subs({x: minGoalx}) >= minGoaly
intersectsGoal_max = fxy.subs({x: maxGoalx}) <= maxGoaly
intersectsGoal = intersectsGoal_min & intersectsGoal_max
constraints = intersectsGoal
# validCondition1 = (sp.Abs(v0x) > 0) & (sp.sqrt(v0x**2 + v0y**2) >= 7)
# validCondition2 = (fxy.subs({x: minGoal[0]}) >= minGoal[1]) & (fxy.subs({x: maxGoal[0]}) <= maxGoal[1])

netFinalVelocityPiecewise = sp.Piecewise((netFinalVelocity, constraints), (sp.nan, True))
sp.pprint(netFinalVelocityPiecewise)
finalEq = netFinalVelocityPiecewise.subs({startx: 0, starty: 0, minGoalx: 2, minGoaly: 2, maxGoalx: 3, maxGoaly: 3, g: -9.8})
f = sp.lambdify([v0x, v0y], finalEq)

xValues = np.linspace(0, 20, 200)
yValues = np.linspace(0, 20, 200)
X, Y = np.meshgrid(xValues, yValues)

# The symbolic condition divides by v0x and compares values like "nan >= 2" when
# v0x is 0 or outside the real-valued domain. Restrict the visible surface to the
# physically valid interval where the final-time expression is finite.
valid = (np.abs(X) > 1e-9) & (np.abs(X) <= 20)
Z = np.full_like(X, np.nan, dtype=float)
Z[valid] = f(X[valid], Y[valid])

plt.rcParams['axes3d.mouserotationstyle'] = 'azel'
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('Initial X Velocity')
ax.set_ylabel('Initial Y Velocity')
ax.set_zlabel('Net Velocity at Point in Time')
ax.set_title('Net Velocity at final position')

surface = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
plt.show()