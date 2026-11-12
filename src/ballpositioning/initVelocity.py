import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy import Symbol

start = (0, 5)
end = (14.32, 10.73)
goal = (16, 9)
minGoal = (2, 2)
maxGoal = (3, 3)

g = -9.8

v0x, v0y = sp.symbols("v0x v0y")

x = sp.symbols("x")

xA = v0x
xB = start[0]

t = sp.symbols("t")
fx = xA*t + xB

fx_solutions = sp.solve(sp.Eq(fx, x), t)
ft = fx_solutions[0]

yA = g/2
yB = v0y
yC = start[1]

fy = yA*t**2 + yB*t + yC

fxy = fy.subs(t, ft)

dfx = sp.diff(fx, t)
dfy = sp.diff(fy, t)

finalTime = 10

netVelocity = sp.sqrt(sp.sympify(dfx**2) + sp.sympify(dfy**2))
netFinalVelocity = sp.solve(netVelocity.simplify() - finalTime, t)[0]
validCondition1 = (sp.Abs(v0x) > 0) & (sp.sqrt(v0x**2 + v0y**2) >= 7)
validCondition2 = (fxy.subs({x: minGoal[0]}) >= minGoal[1]) & (fxy.subs({x: maxGoal[0]}) <= maxGoal[1])
netFinalVelocityPiecewise = sp.Piecewise((netFinalVelocity, validCondition1 and validCondition1), (sp.nan, True))
print(netFinalVelocity)
f = sp.lambdify([v0x, v0y], netFinalVelocityPiecewise)

xValues = np.linspace(0, 20, 100)
yValues = np.linspace(0, 20, 100)
X, Y = np.meshgrid(xValues, yValues)

# The symbolic condition divides by v0x and compares values like "nan >= 2" when
# v0x is 0 or outside the real-valued domain. Restrict the visible surface to the
# physically valid interval where the final-time expression is finite.
valid = (np.abs(X) > 1e-9) & (np.abs(X) <= 10)
Z = np.full_like(X, np.nan, dtype=float)
Z[valid] = f(X[valid], Y[valid])

plt.rcParams['axes3d.mouserotationstyle'] = 'azel'
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('Initial X Velocity')
ax.set_ylabel('Initial Y Velocity')
ax.set_zlabel('Net Velocity at Point in Time')

surface = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
plt.show()