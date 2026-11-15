import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

"""
Forward Euler Method
L: lalplacian matrix
u0: initial condition
f: forcing function
T: Total time
Nt: number of time steps
"""
def forward_euler(L, u0, f, T, M):
    dt = T / M
    u = u0.copy()
    for n in range(M):
        u = u + dt * (L @ u + f(n * dt))
    return u

def backward_euler(L, u0, f, T, M):
    dt = T / M
    u = u0.copy()
    I = sp.identity(L.shape[0], format='csc')
    solve = spla.factorized((I - dt * L).tocsc())
    for n in range(M):
        b = u + dt * f((n+1) * dt)
        u = solve(b)
    return u

def crank_nicolson(L, u0, f, T, M):
    dt = T / M
    u = u0.copy()
    I = sp.identity(L.shape[0], format='csc')
    solve = spla.factorized((I - 1/2 * dt * L).tocsc())
    for n in range(M):
        b = u + 1/2 * dt * (f((n+1)*dt) + L @ u + f(n * dt))
        u = solve(b)
    return u

def explicit_midpoint(L, u0, f, T, M):
    dt = T / M
    u = u0.copy()
    for n in range(M):
        u_half = u + 1/2 * dt * (L @ u + f(n * dt))
        u = u + dt * (L @ u_half + f((n + 1/2) * dt))
    return u

def BDF2(L, u0, f, T, M):
    dt = T / M
    I = sp.identity(L.shape[0], format='csc')
    be_solve = spla.factorized((I - dt * L).tocsc())
    u_prev = u0.copy()
    u = be_solve(u_prev + dt * f(dt))
    solve = spla.factorized((2 * dt * L - 3*I).tocsc())
    for n in range(1, M):
        b = -4 * u + u_prev - 2 * dt * f((n+1) * dt)
        u_prev, u = u, solve(b)
    return u


def laplacian(Nx, Ny, dx, dy):
    nx, ny = Nx - 1, Ny - 1 
    Ix, Iy = sp.identity(nx), sp.identity(ny)
    return (sp.kron(D2(nx, dx), Iy) + sp.kron(Ix, D2(ny, dy))).tocsr()

def D2(m, h):
        return sp.diags([1.0, -2.0, 1.0], [-1, 0, 1], shape=(m, m)) / h**2