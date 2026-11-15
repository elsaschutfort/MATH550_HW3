import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import timestepping as ts
import matplotlib.pyplot as plt

MValsFE = [4096, 8192, 16384, 32768]
NVals = [64, 128]

u_exact_func = lambda x, y, t: np.cos(10 * t) * np.sin(x) * np.sin(y)
f_func = lambda x, y, t: (2*np.cos(10*t) - 10*np.sin(10*t)) * (np.sin(x) * np.sin(y))
u0_func = lambda x, y: np.sin(x) * np.sin(y)
T = 2 * np.pi
results = []


for N in NVals:
    dx = 2*np.pi / N
    L = ts.laplacian(N, N, dx, dx)

    x = np.linspace(0, T, N+1)[1:-1]
    X, Y = np.meshgrid(x, x, indexing='ij')
    u0 = u0_func(X, Y).ravel()
    f = lambda t: f_func(X, Y, t).ravel()
    u_exact = u_exact_func(X, Y, T).ravel()

    dts, errs = [], []
    for M in MValsFE:
        u_approx = ts.forward_euler(L, u0, f, T, M)
        errs.append(np.linalg.norm(u_approx - u_exact) / np.linalg.norm(u_exact))
        dts.append(T / M)
    results.append((np.array(dts), np.array(errs)))

dts = np.array(dts)
errs = np.array(errs)

plt.loglog(results[0][0], results[0][1], 'o-', label='N = 64')
plt.loglog(results[1][0], results[1][1], 'o-', label='N = 64')
plt.loglog(dts, errs[0]*dts/dts[0], 'k--', label=r'O($\Delta$t)')
plt.xlabel(r'$\Delta$t')
plt.ylabel('relative error')
plt.legend()
plt.show()