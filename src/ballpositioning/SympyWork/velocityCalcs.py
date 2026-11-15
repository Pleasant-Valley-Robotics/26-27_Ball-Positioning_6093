import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy import Symbol

start = (0, 5)
end = (14.32, 10.73)
goal = (16, 9)

# g = sp.symbols("g")
g = -9.8

v0x, v0y = sp.symbols("v0x v0y")
x = sp.symbols("x")

xA = v0x
xB = start[0]

t = sp.symbols("t")
fx = xA*t + xB

fx_solutions = sp.solve(sp.Eq(fx, x), t)
ft = fx_solutions[0].subs(x, t)

yA = g/2
yB = v0y
yC = start[1]

fy = yA*t**2 + yB*t + yC

yRoots = sp.solve(fy, t)

# yMaxTime = sum(yRoots) / len(yRoots)
yMaxTime = - yB / (2*yA)

dfx = sp.diff(fx, t)
dfy = sp.diff(fy, t)

fxy = fy.subs(t, ft)

v0yValue = sp.solve(fy.subs(t, yMaxTime) - goal[1], v0y)[1]
# print(fy.subs(t, yMaxTime) - goal[1])

v0xValue = sp.solve(fx.subs({t: yMaxTime, v0y: v0yValue}) - goal[0], v0x)[0]

dfxy = sp.diff(fxy, t)
theta = sp.atan(dfxy)

netVelocity = sp.sqrt(sp.sympify(dfx**2) + sp.sympify(dfy**2))
netFinalVelocity = sp.solve(netVelocity, t)[0]
print(netFinalVelocity)
f = sp.lambdify([v0x, v0y], netFinalVelocity)

xValues = np.linspace(0, 10, 100)
yValues = np.linspace(0, 10, 100)
X, Y = np.meshgrid(xValues, yValues)
Z = f(X, Y)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

surface = ax.plot_surface(X, Y, Z)
plt.show()

dtheta = sp.diff(theta, t)

print(v0xValue, v0yValue)
print(theta.subs({t: 0, v0x: v0xValue, v0y: v0yValue}))

# vT = sp.sqrt(dfx**2 + sp.diff(fy, t)**2)