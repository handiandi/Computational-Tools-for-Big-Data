#!/usr/bin/env python3

import numpy as np

"""
This file loads a matrix from a file ("matrix.txt") and compute the equation Ax = b where b is the last column of the matrix and A is the other columns
"""
matrix = np.loadtxt("matrix.txt", delimiter=",") #Loads the file of matrix
b = matrix[:,len(matrix)]  #Extract the last column of the matrix
A = matrix[:,:len(matrix)] #Remove the last column from the matrix

x = np.linalg.solve(A, b) #Solve the equation using linalg.solve in numpy
print("The answer is {0}".format(x))
