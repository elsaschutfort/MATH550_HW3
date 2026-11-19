import numpy as np
import timestepping as ts
import math

def cost(Nt, mult, step, N=62**2):
    return Nt * (mult*5*N + step*N*np.log(N)) 

# print(cost(2608, 1, 0))
# print(cost(2608, 2, 0))
# print(cost(151, 0, 1))
# print(cost(81 , 1, 1))
# print(cost(156 , 0, 1))
# Backward Euler mult: 0 step: 1
# CN: mult: 1 step: 1
# BDF2 mult: 0 step: 1

# print(cost(5997, 1, 0)) 
# print(cost(2608, 2, 0)) # Explicit Midpoint
# print(cost(6078, 0, 1))
# print(cost(563 , 1, 1))# Crank
# print(cost(1129 , 0, 1))#BDF2

print(cost(5288, 2, 0)) # Explicit Midpoint
print(cost(7955, 1, 1)) # Crank
print(cost(15914 , 0, 1)) #BDF2

print(cost(1207446, 0, 1))