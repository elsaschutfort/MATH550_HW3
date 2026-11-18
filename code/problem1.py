import numpy as np
import timestepping as ts
import matplotlib.pyplot as plt

NValsFE = {64:  [2800, 5600, 11200, 22400, 44800],
         128: [10432*x for x in range(1, 7)]}
NValsEM = {64:  [2800, 5600, 11200, 22400],
         128: [11200, 22400, 44800, 89600]}

NValsBE = {64: 2**np.arange(9, 17), 
           128: 2**np.arange(9, 17)}
NValsCN = {64: 2**np.arange(6, 15), 
           128: 2**np.arange(6, 15)}
NValsBD = {64: 2**np.arange(8, 15), 
           128: 2**np.arange(8, 15)}

STYLES = {
    64: dict(color='C0', linestyle='-', marker='o', linewidth=3),
    128: dict(color='C1', linestyle='--', marker='x', linewidth=4)
}
u_exact_func = lambda x, y, t: np.cos(10 * t) * np.sin(x) * np.sin(y)
T = 2 * np.pi
feResults = ts.time_stepping(T, u_exact_func, NValsFE, ts.forward_euler)
beResults = ts.time_stepping(T, u_exact_func, NValsBE, ts.backward_euler)
cnResults = ts.time_stepping(T, u_exact_func, NValsCN, ts.crank_nicolson)
emResults = ts.time_stepping(T, u_exact_func, NValsEM, ts.explicit_midpoint)
bdf2Results = ts.time_stepping(T, u_exact_func, NValsBD, ts.BDF2)

def plot_convergence(ax, results, order, title):
    all_dts = []
    for N, (dts, errs) in results.items():
        ax.loglog(dts, errs, markersize=8, label=f'N = {N}', **STYLES[N])
        all_dts.extend(dts)
    all_dts = np.sort(all_dts)

    k = len(dts) // 2
    ref = errs[k] * (all_dts / dts[k])**order

    if order == 1:
        label = r'O($\Delta t$)'
    else: 
        label = r'O($\Delta t^2$)'
    ax.loglog(all_dts, ref, 'k:', linewidth=3, label=label)

    ax.set_title(title)
    ax.set_xlabel(r'$\Delta t$')
    ax.set_ylabel('Relative Error')
    ax.legend()


fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.ravel()

plot_convergence(axes[0], feResults,   1, "Relative Error of Forward Euler Method")
plot_convergence(axes[1], beResults,   1, "Relative Error of Backward Euler Method")
plot_convergence(axes[2], cnResults,   2, "Relative Error of Crank Nicolson Method")
plot_convergence(axes[3], emResults,   2, "Relative Error of Explicit Midpoint Method")
plot_convergence(axes[4], bdf2Results, 2, "Relative Error of BDF2 Method")

axes[-1].axis('off')
fig.tight_layout()
plt.show()