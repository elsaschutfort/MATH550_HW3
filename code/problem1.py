import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import timestepping as ts
import matplotlib.pyplot as plt

NValsFE = {64:  [2800, 5600, 11200, 22400, 44800],
         128: [11200, 22400, 44800, 89600]}
allDTS = np.array([2800, 5600, 11200, 22400, 44800, 89600])
NValsBE = {64: 2**np.arange(4, 16), 
           128: 2**np.arange(4, 16)}

results = {}

u_exact_func = lambda x, y, t: np.cos(10 * t) * np.sin(x) * np.sin(y)
T = 2 * np.pi


results['Forward Euler'] = ts.time_stepping(T, u_exact_func, NValsFE, ts.forward_euler)
#results['Backward Euler'] = ts.time_stepping(T, u_exact_func, NValsBE, ts.backward_euler)
#results['Crank-Nicolson'] = ts.time_stepping(T, u_exact_func, NValsBE, ts.crank_nicolson)
#results['Explicit Midpoint'] = ts.time_stepping(T, u_exact_func, NValsFE, ts.explicit_midpoint)
#results['BDF2'] = ts.time_stepping(T, u_exact_func, NValsBE, ts.BDF2)


fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.ravel()

for ax, (name, res) in zip(axes, results.items()):
    all_dts, all_errs = [], []
    for N, (dts, errs) in res.items():
        ax.loglog(dts, errs, 'o-', linewidth=3, label=f'N = {N}')
        all_dts.extend(dts)
        all_errs.extend(errs)

    all_dts = np.array(all_dts)
    all_errs = np.array(all_errs)
    ax.loglog(all_dts, all_errs[0]*all_dts/all_dts[0], 'k--', linewidth=3, label=r'O($\Delta t$)')
    ax.set_title(f'Relative Error of {name} Method')
    ax.set_xlabel(r'$\Delta t$')
    ax.set_ylabel('Relative Error')
    ax.legend()

axes[-1].axis('off')
fig.tight_layout()
plt.show()