# HW 3: Time Stepping

## Setup
For the set up, a major part of it related to the use of the code and not related to the actual coding of the 5 time stepping methods. For the derivation, plug $$u = \cos (10t) \sin (x) \sin (y)$$ into the PDE to get $$f = (2 \cos 10t - 10 \sin 10t) \sin (x) \sin (y)$$, with $$u = 0$$ on all four edges and $$u(x, y, 0) = \sin (x) \sin (y)$$. Discretizing spatially gives 
$$\frac{du}{dt} = Lu(t) + f(t)$$
so we need to find the discrete forcing function. 

## Problem 1 Relative Error

| ![Surface plot of the Problem 1 solution](figures/Problem1.png) |
| :-: |
| *Figure 1: Relative Error for all 5 time stepping methods.$ |

## Problem 2 

| Method | Number of Steps | Cost |
|------|-------------|------|
| Forward Euler | 2608 | 50,125,760 |
| Backward Euler | 151 | 5,029,468 |
| Crank Nicolson | 81 | 4,365,230 |
| Explicit Midpoint | 2608 | 100,251,520 |
| BDF2 | 156 | 5,188,115 |

| Method | Number of Steps | Cost |
|------|-------------|------|
| Forward Euler | 5997 | 115,262,340 |
| Backward Euler | 6078 | 193,089,676 |
| Crank Nicolson | 563 | 28,922,845 |
| Explicit Midpoint | 2608 | 100,251,520 |
| BDF2 | 1129 | 36,060,830 |

| Method | Number of Steps | Cost |
|------|-------------|------|
| Backward Euler | 1207446 | 38,311,786,491 |
| Crank Nicolson | 7955 | 405,540,877 |
| Explicit Midpoint | 5288 | 203,270,720 |
| BDF2 | 15914 | 505,180,145 |