#!/usr/bin/env python3
import numpy as np
import scipy as sp
import scipy.interpolate
import scipy.optimize
import matplotlib.pyplot as plt

# extract x and y points from text file
np_array = np.loadtxt("list_of_points.txt")
# create numpy arrays with x and y points
x_array = np_array[:,0]
y_array = np_array[:,1]

# run interp1d to interpolate a 1-d function
f = scipy.interpolate.interp1d(x_array, y_array)

xnew = np.linspace(-20, 19)
# plot data and function for x points
plt.plot(x_array, y_array, 'o', xnew, f(xnew), '-')
plt.legend(['data', 'interpolation'], loc='best')
plt.show()


# finding roots
res = scipy.optimize.root(f,[0])
print(res.x)