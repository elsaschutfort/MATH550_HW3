import numpy as np
import timestepping as ts
import math

N = 64
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

def largest_deltat(tol, method, min_Nt, max_Nt=2**17):
    if (rel_errors(min_Nt, method) <= tol):
        return min_Nt
    if (rel_errors(max_Nt, method) > tol):
        return None
    while (min_Nt + max_Nt) > 1:
        mid_Nt = (min_Nt + max_Nt) // 2
        if (rel_errors(mid_Nt, method) <= tol):
            max_Nt = mid_Nt
        if (rel_errors(mid_Nt, method) > tol):
            min_Nt = mid_Nt
    return mid_Nt


