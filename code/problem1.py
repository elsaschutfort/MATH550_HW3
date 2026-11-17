import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import timestepping as ts
import matplotlib.pyplot as plt

NValsFE = {64:  [2610*x for x in range(1, 7)],
         128: [10432*x for x in range(1, 7)]}
NValsEM = {64:  [2800, 5600, 11200, 22400],
         128: [11200, 22400, 44800, 89600]}

NValsBE = {64: 2**np.arange(5, 15), 
           128: 2**np.arange(5, 15)}
NValsCN = {64: 2**np.arange(3, 14), 
           128: 2**np.arange(3, 14)}
u_exact_func = lambda x, y, t: np.cos(10 * t) * np.sin(x) * np.sin(y)
T = 2 * np.pi
feResults = ts.time_stepping(T, u_exact_func, NValsFE, ts.forward_euler)
beResults = ts.time_stepping(T, u_exact_func, NValsBE, ts.backward_euler)
cnResults = ts.time_stepping(T, u_exact_func, NValsCN, ts.crank_nicolson)
emResults = ts.time_stepping(T, u_exact_func, NValsEM, ts.explicit_midpoint)
bdf2Results = ts.time_stepping(T, u_exact_func, NValsCN, ts.BDF2)


fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.ravel()

all_dts, all_errs = [], []
for N, (dts, errs) in feResults.items():
    axes[0].loglog(dts, errs, 'o-', linewidth=3, label=f'N = {N}')
    all_dts.extend(dts)
    all_errs.extend(errs)
all_dts = np.array(all_dts)
all_errs = np.array(all_errs)
axes[0].loglog(all_dts, (all_errs[0]*all_dts/all_dts[0]), 'k--', linewidth=3, label=r'O($\Delta t$)')
axes[0].set_title(f'Relative Error of Forward Euler Method')
axes[0].set_xlabel(r'$\Delta t$')
axes[0].set_ylabel('Relative Error')
axes[0].legend()

for N, (dts, errs) in beResults.items():
    axes[1].loglog(dts, errs, 'o-', linewidth=3, label=f'N = {N}')
axes[1].loglog(dts, (errs[0]*dts/dts[0]), 'k--', linewidth=3, label=r'O($\Delta t$)')
axes[1].set_title(f'Relative Error of Backward Euler Method')
axes[1].set_xlabel(r'$\Delta t$')
axes[1].set_ylabel('Relative Error')
axes[1].legend()

for N, (dts, errs) in cnResults.items():
    axes[2].loglog(dts, errs, 'o-', linewidth=3, label=f'N = {N}')
axes[2].loglog(dts, (errs[0]*dts/dts[0])**(2), 'k--', linewidth=3, label=r'O($\Delta t^2$)')
axes[2].set_title(f'Relative Error of Crank Nicolson Method')
axes[2].set_xlabel(r'$\Delta t$')
axes[2].set_ylabel('Relative Error')
axes[2].legend()

all_dts, all_errs = [], []
for N, (dts, errs) in emResults.items():
    axes[3].loglog(dts, errs, 'o-', linewidth=3, label=f'N = {N}')
    all_dts.extend(dts)
    all_errs.extend(errs)
all_dts = np.array(all_dts)
all_errs = np.array(all_errs)
axes[3].loglog(all_dts, (all_errs[0]*all_dts/all_dts[0]), 'k--', linewidth=3, label=r'O($\Delta t^2$)')
axes[3].set_title(f'Relative Error of Explicit Midpoint Method')
axes[3].set_xlabel(r'$\Delta t$')
axes[3].set_ylabel('Relative Error')
axes[3].legend()

for N, (dts, errs) in bdf2Results.items():
    axes[4].loglog(dts, errs, 'o-', linewidth=3, label=f'N = {N}')
axes[4].loglog(dts, (errs[0]*dts/dts[0])**(2), 'k--', linewidth=3, label=r'O($\Delta t^2$)')
axes[4].set_title(f'Relative Error of BDF2 Method')
axes[4].set_xlabel(r'$\Delta t$')
axes[4].set_ylabel('Relative Error')
axes[4].legend()

axes[-1].axis('off')
fig.tight_layout()
plt.show()