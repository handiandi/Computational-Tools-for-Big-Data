#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import os
import numpy as np
cimport numpy as np
import timeit

ctypedef np.int_t DTYPE_t

# parameters
FILENAME = "data_100points_100dims.dat"

EPS = 0.15
M = 2

def run_program():
	file_handler = open(os.path.join("data",FILENAME),"rb")
	cdef np.ndarray[DTYPE_t, ndim=2] X = pickle.load(file_handler, encoding="latin1").todense()
	file_handler.close()

	cdef np.ndarray[DTYPE_t, ndim=1] visited_indexes = np.zeros(X.shape[0], dtype=np.int64)
	cdef np.ndarray[DTYPE_t, ndim=1] cluster_indexes = np.zeros(X.shape[0], dtype=np.int64)
	
	db_scan(EPS, M, X, cluster_indexes, visited_indexes)
	print(cluster_indexes)
	print(np.unique(cluster_indexes).size)

def db_scan(double eps, int m, np.ndarray[DTYPE_t, ndim=2] X, np.ndarray[DTYPE_t, ndim=1] cluster_indexes, np.ndarray[DTYPE_t, ndim=1] visited_indexes):
	cdef int p_index, C = 0
	cdef int num_rows = X.shape[0]
	for p_index in range(0, num_rows):
		if visited_indexes[p_index]:
			continue
		visited_indexes[p_index] = 1
		neighbor_points = region_query(p_index, eps, X)
		if neighbor_points.size < m:
			cluster_indexes[p_index] = -1
		else:
			C += 1
			expand_cluster(p_index, neighbor_points, C, eps, m, X, cluster_indexes, visited_indexes)

def expand_cluster(int p_index, np.ndarray[DTYPE_t, ndim=1] neighbor_points, int C, double eps, int m, np.ndarray[DTYPE_t, ndim=2] X, np.ndarray[DTYPE_t, ndim=1] cluster_indexes, np.ndarray[DTYPE_t, ndim=1] visited_indexes):
	cluster_indexes[p_index] = C
	cdef int i = 0
	while i < neighbor_points.size:
		if not visited_indexes[neighbor_points[i]]:
			visited_indexes[neighbor_points[i]] = 1
			neighbor_points_prime = region_query(neighbor_points[i], eps, X)
			if neighbor_points_prime.size >= m:
				neighbor_points = np.append(neighbor_points, neighbor_points_prime)
		if cluster_indexes[neighbor_points[i]] == 0:
			cluster_indexes[neighbor_points[i]] = C
		i += 1

def compute_jaccard_distance(np.ndarray[DTYPE_t, ndim=2] A, np.ndarray[DTYPE_t, ndim=2] B):
	M_11 = np.sum(np.multiply(A,B))
	M_01_and_M_10 = np.sum(np.absolute((A-B)))
	jaccard_index = (M_11)/ float((M_01_and_M_10 + M_11))
	jaccard_distance = 1 - jaccard_index
	return jaccard_distance

def region_query(int p_index, double eps, np.ndarray[DTYPE_t, ndim=2] X):
	""" compute distance for every row other than X(index)
		if distance < eps, keep neighbour as index
	"""
	cdef np.ndarray[DTYPE_t, ndim=1] neighbor_indexes = np.zeros(X.shape[0], dtype=np.int64)
	cdef int i = 0
	cdef int num_rows = X.shape[0]
	for i in range(0, num_rows):
		distance = compute_jaccard_distance(X[i,:], X[p_index,:])
		if distance <= eps:
			neighbor_indexes[i] = 1
	# why does it return tuple, fix this
	return neighbor_indexes.nonzero()[0]


print(timeit.timeit(run_program, number=1))

#assert (np.array([ 1,  2, -1,  3,  4, -1,  4,  4, -1,  4, -1,  2,  2,  1, -1,  1,  1,  4,
# -1,  1,  2,  1,  1,  4, -1, -1,  2,  2,  1,  4,  4,  4,  4,  1, -1, -1,
#  2,  1, -1,  4,  1, -1,  2,  1,  1,  4,  4,  4,  4,  1,  2,  4,  2,  4,
# -1,  1,  4, -1,  3, -1, -1,  1, -1, -1,  4, -1,  2,  2,  3,  5,  1, -1,
#  1,  4, -1,  2,  2,  4, -1, -1,  1,  4, -1, -1,  5,  2,  2,  1, -1,  1,
# -1,  1, -1,  1, -1,  2,  1, -1,  2,  2,]) == cluster_indexes).all()