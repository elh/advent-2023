from sympy import symbols, Eq, solve

"""
given equations of the form:
x = dx * t + x0
y = dy * t + y0
z = dz * t + z0

solve for dx, x0, dy, y0, dz, z0.
add enough equations to solve for all variables.
"""

t1, t2, t3, dx, x0, dy, y0, dz, z0 = symbols("t1 t2 t3 dx x0 dy y0 dz z0")

# Example data
eq_x_1 = Eq(dx * t1 + x0, -2 * t1 + 19)
eq_y_1 = Eq(dy * t1 + y0, 1 * t1 + 13)
eq_z_1 = Eq(dz * t1 + z0, -2 * t1 + 30)

eq_x_2 = Eq(dx * t2 + x0, -1 * t2 + 18)
eq_y_2 = Eq(dy * t2 + y0, -1 * t2 + 19)
eq_z_2 = Eq(dz * t2 + z0, -2 * t2 + 22)

eq_x_3 = Eq(dx * t3 + x0, -2 * t3 + 20)
eq_y_3 = Eq(dy * t3 + y0, -2 * t3 + 25)
eq_z_3 = Eq(dz * t3 + z0, -4 * t3 + 34)

soln = solve(
    [eq_x_1, eq_y_1, eq_z_1, eq_x_2, eq_y_2, eq_z_2, eq_x_3, eq_y_3, eq_z_3],
    [t1, t2, t3, dx, x0, dy, y0, dz, z0],
    domain="ZZ",
    dict=True,
)

print(soln)
print(soln[0][dx])
