import numpy as np
import timestepping as ts
import math

N = 128
T = 2 * np.pi
dx = 2*np.pi / N
u_exact_func = lambda x, y, t: np.cos(10 * t) * np.sin(x) * np.sin(y)
L = ts.laplacian(N, N, dx, dx)
x = np.linspace(0, T, N+1)[1:-1]
X, Y = np.meshgrid(x, x, indexing='ij')
sines = (np.sin(X) * np.sin(Y)).ravel()

u0 = sines.copy()
lam = (8 / dx**2) * (np.sin(dx / 2) ** 2)
f = lambda t, sines=sines: (lam*np.cos(10*t) - 10*np.sin(10*t)) * sines
u_exact = u_exact_func(X, Y, T).ravel()


def rel_errors(Nt, method, T=2*np.pi, u_exact=u_exact, L=L, u0=u0, f=f):
    u_approx = method(L, u0, f, T, Nt)
    return np.linalg.norm(u_approx - u_exact) / np.linalg.norm(u_exact)

def minimum_stable_Nt(N):
    return math.ceil(2 * N**2 / np.pi)

def largest_deltat(tol, method, min_Nt, max_Nt=2**18):
    if (rel_errors(min_Nt, method) <= tol):
        return min_Nt
    if (rel_errors(max_Nt, method) > tol):
        return None
    while (max_Nt - min_Nt) > 1:
        mid_Nt = (min_Nt + max_Nt) // 2
        if (rel_errors(mid_Nt, method) <= tol):
            max_Nt = mid_Nt
        else:
            min_Nt = mid_Nt
    return max_Nt

tols = [5e-2, 1e-3, 5e-6]
explicit_methods = [(ts.forward_euler, "Forward Euler"), (ts.explicit_midpoint, "Explicit Midpoint")]
implicit_methods = [(ts.backward_euler, "Backward Euler"), (ts.crank_nicolson, "Crank"), (ts.BDF2, "BDF2")]
min_Nt = minimum_stable_Nt(N)

# for tol in tols:
#     for (method, name) in explicit_methods:
#         smallest_Nt = largest_deltat(tol, method, min_Nt)
#         if smallest_Nt != None:
#             print(f"tol: {tol} N: {smallest_Nt} name: {name}")

#     for (method, name) in implicit_methods:
#         smallest_Nt = largest_deltat(tol, method, 32)
#         if smallest_Nt != None:
#             print(f"tol: {tol} N: {smallest_Nt} name: {name}")


min_Nt = minimum_stable_Nt(N)

# for (method, name) in explicit_methods:
#     for tol in tols:
#         smallest_Nt = largest_deltat(tol, method, min_Nt)
#         print(f"tol: {tol} N: {smallest_Nt} name: {name}")

# for (method, name) in implicit_methods:
#     for tol in tols:
#         smallest_Nt = largest_deltat(tol, method, 32)
#         print(f"tol: {tol} N: {smallest_Nt} name: {name}")

# for tol in tols:
#     smallest_Nt = largest_deltat(tol, ts.BDF2, 32)
#     print(f"tol: {tol} N: {smallest_Nt}")

print(rel_errors(2**21, ts.backward_euler, 32))
