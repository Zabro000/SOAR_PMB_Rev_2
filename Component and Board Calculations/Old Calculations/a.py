from sympy import symbols
from sympy.plotting import plot
from sympy.integrals import laplace_transform



"""x, u ,s = symbols('x u s') 
f = sy.exp(-(x - u) ** 2 / (2 * s ** 2)) / (s * (2 * sy.pi) ** (1/2))

ix = sy.integrate(f,x)
print(ix)
r = ix.subs(x, 10).subs(u, 1).subs(s, 10)
print(float(r))"""


from sympy import laplace_transform, diff, Function
from sympy import laplace_correspondence, laplace_initial_conds
from sympy.abc import t, s
y = Function("y")
Y = Function("Y")
f = laplace_transform(diff(y(t), t, 3), t, s, noconds=True)
g = laplace_correspondence(f, {y: Y})
print(laplace_initial_conds(g, t, {y: [2, 4, 8, 16, 32]}))


