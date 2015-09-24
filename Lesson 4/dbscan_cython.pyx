#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True
#cython: nonecheck=False
#cython: profile=True

import pstats, cProfile
import pickle
import os
import numpy as np
cimport numpy as np
import timeit

ctypedef np.int_t DTYPE_t



def run_program():
	# parameters
	FILENAME = "data_100points_100dims.dat"
	cdef float EPS = 0.3
	cdef int M = 2

	file_handler = open(os.path.join("data",FILENAME),"rb")
	cdef np.ndarray[DTYPE_t, ndim=2] X = pickle.load(file_handler, encoding="latin1").todense()
	file_handler.close()

	cdef np.ndarray[np.float_t, ndim=2] distance_matrix = np.empty((X.shape[0],X.shape[1]), dtype=np.float64)
	distance_matrix.fill(-1)

	cdef np.ndarray[DTYPE_t, ndim=1] visited_indexes = np.zeros(X.shape[0], dtype=np.int64)
	cdef np.ndarray[DTYPE_t, ndim=1] cluster_indexes = np.zeros(X.shape[0], dtype=np.int64)
	
	db_scan(EPS, M, X, cluster_indexes, visited_indexes, distance_matrix)
	print(cluster_indexes)
	print(np.unique(cluster_indexes).size)

def db_scan(float eps, int m, np.ndarray[DTYPE_t, ndim=2] X, np.ndarray[DTYPE_t, ndim=1] cluster_indexes, np.ndarray[DTYPE_t, ndim=1] visited_indexes, np.ndarray[np.float_t, ndim=2] distance_matrix):
	cdef int p_index, C = 0
	cdef int num_rows = X.shape[0]
	for p_index in range(0, num_rows):
		if visited_indexes[p_index]:
			continue
		visited_indexes[p_index] = 1
		neighbor_points = region_query(p_index, eps, X, distance_matrix)
		if neighbor_points.size < m:
			cluster_indexes[p_index] = -1
		else:
			C += 1
			expand_cluster(p_index, neighbor_points, C, eps, m, X, cluster_indexes, visited_indexes, distance_matrix)

def expand_cluster(int p_index, np.ndarray[DTYPE_t, ndim=1] neighbor_points, int C, float eps, int m, np.ndarray[DTYPE_t, ndim=2] X, np.ndarray[DTYPE_t, ndim=1] cluster_indexes, np.ndarray[DTYPE_t, ndim=1] visited_indexes, np.ndarray[np.float_t, ndim=2] distance_matrix):
	cluster_indexes[p_index] = C
	cdef int i = 0
	while i < neighbor_points.size:
		index = neighbor_points[i]
		if not visited_indexes[index]:
			visited_indexes[index] = 1
			neighbor_points_prime = region_query(index, eps, X, distance_matrix)
			if neighbor_points_prime.size >= m:
				neighbor_points = np.append(neighbor_points, neighbor_points_prime)
		if cluster_indexes[index] == 0:
			cluster_indexes[index] = C
		i += 1

def compute_jaccard_distance(np.ndarray[DTYPE_t, ndim=2] X, np.ndarray[np.float_t, ndim=2] distance_matrix, int a_index, int b_index):
	cdef int M_11, M_01_and_M_10
	cdef float jaccard_index, jaccard_distance

	X_a_index_row = X[a_index,:]
	X_b_index_row = X[b_index,:]
	M_11 = np.sum(np.multiply(X_a_index_row,X_b_index_row))
	M_01_and_M_10 = np.sum(np.absolute((X_a_index_row-X_b_index_row)))
	jaccard_index = (M_11)/ float((M_01_and_M_10 + M_11))
	jaccard_distance = 1 - jaccard_index
	
	distance_matrix[a_index, b_index] = jaccard_distance
	distance_matrix[b_index, a_index] = jaccard_distance
	return jaccard_distance

def region_query(int p_index, float eps, np.ndarray[DTYPE_t, ndim=2] X, np.ndarray[np.float_t, ndim=2] distance_matrix):
	""" compute distance for every row other than X(index)
		if distance < eps, keep neighbour as index
	"""
	cdef np.ndarray[DTYPE_t, ndim=1] neighbor_indexes = np.zeros(X.shape[0], dtype=np.int64)
	cdef int i = 0
	cdef float distance = 0.0
	cdef int num_rows = X.shape[0]
	for i in range(0, num_rows):
		if (distance_matrix[i,p_index] != -1):
			distance = distance_matrix[p_index, i]
		elif (distance_matrix[p_index, i] != -1):
			distance = distance_matrix[p_index, i]
		else:
			distance = compute_jaccard_distance(X, distance_matrix, i, p_index)
		if distance <= eps:
			neighbor_indexes[i] = 1
	# why does it return tuple, fix this
	return neighbor_indexes.nonzero()[0]

cProfile.runctx("run_program()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("tottime").print_stats()

#print(timeit.timeit(run_program, number=1))

#assert (np.array([ 1,  2, -1,  3,  4, -1,  4,  4, -1,  4, -1,  2,  2,  1, -1,  1,  1,  4,
# -1,  1,  2,  1,  1,  4, -1, -1,  2,  2,  1,  4,  4,  4,  4,  1, -1, -1,
#  2,  1, -1,  4,  1, -1,  2,  1,  1,  4,  4,  4,  4,  1,  2,  4,  2,  4,
# -1,  1,  4, -1,  3, -1, -1,  1, -1, -1,  4, -1,  2,  2,  3,  5,  1, -1,
#  1,  4, -1,  2,  2,  4, -1, -1,  1,  4, -1, -1,  5,  2,  2,  1, -1,  1,
# -1,  1, -1,  1, -1,  2,  1, -1,  2,  2,]) == cluster_indexes).all()