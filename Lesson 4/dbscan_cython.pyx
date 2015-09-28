#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#cython: boundscheck=False
#cython: wraparound=False
#cython: initializedcheck=False

import pstats, cProfile
import pickle
import os
import numpy as np
cimport numpy as np
import timeit
import sys

DTYPE = np.int
DTYPE_FLOAT = np.float
ctypedef np.int_t DTYPE_t
ctypedef np.float_t DTYPE_FLOAT_t

    # parameters
FILENAME = "data_100000points_100000dims.dat"
cdef float EPS = 0.15
cdef int M = 2

file_handler = open(os.path.join("data",FILENAME),"rb")
X = pickle.load(file_handler, encoding="latin1")
file_handler.close()

cdef int [:] indices_view = X.indices.astype(np.dtype("i"))

cdef int [:] indptr_view = X.indptr.astype(np.dtype("i"))

cdef float [:] data_view = X.data.astype(np.dtype("f"))

cdef int num_rows = X.get_shape()[0]
cdef int num_cols = X.get_shape()[1]


neighbor_indexes = np.empty((num_rows), dtype=np.dtype("i"))
cdef int [:] neighbor_indexes_view = neighbor_indexes


#distance_matrix_np = np.empty((num_rows,num_cols), dtype=np.dtype("double"))
#distance_matrix_np.fill(-1)
#cdef double [:,:] distance_matrix = distance_matrix_np

cdef int [:] visited_indexes = np.zeros(num_rows, dtype=np.dtype("i"))
cdef int [:] cluster_indexes = np.zeros(num_rows, dtype=np.dtype("i"))

def run_program():
    db_scan(EPS, M)

    print(np.array(cluster_indexes))
    print("Number of clusters: {0}".format(np.unique(cluster_indexes).size))
    print("Number of points in the largest cluster: {0}".format(np.max(np.unique(cluster_indexes, return_counts=True)[1])))

def db_scan(float eps, int m):
    cdef int p_index, C = 0
    for p_index in range(num_rows):
        # check if visited
        if visited_indexes[p_index]:
            continue
        visited_indexes[p_index] = 1
        neighbor_points = region_query(p_index, eps)
        # check if smaller than m-1 since we dont return P
        if len(neighbor_points) < m-1:
            cluster_indexes[p_index] = -1
        else:
            C += 1
            expand_cluster(p_index, neighbor_points, C, eps, m)

def expand_cluster(int p_index, np.ndarray[DTYPE_t, ndim=1] neighbor_points, int C, float eps, int m):  #np.ndarray[DTYPE_t, ndim=1] 
    cluster_indexes[p_index] = C
    cdef int i = 0
    cdef int index = 0
    #print(len(visited_indexes))
    while i < neighbor_points.size:
        index = neighbor_points[i]
        #print(index)
        if not visited_indexes[index]:
            visited_indexes[index] = 1
            neighbor_points_prime = region_query(index, eps)
            # check if smaller than m-1 since we dont return P
            if neighbor_points_prime.size >= m-1:
                neighbor_points = np.append(neighbor_points, neighbor_points_prime)

        if cluster_indexes[index] == 0:
            cluster_indexes[index] = C
        i += 1

def compute_jaccard_distance(int a_index, int p_index):
    cdef int M_11 = 0, M_01_and_M_10 = 0
    cdef float jaccard_index, jaccard_distance

    cdef int f_row = indptr_view[a_index] # first column position of value in row 1
    cdef int s_row = indptr_view[p_index] # first column position of value in row 2
    cdef int t_row = indptr_view[p_index+1] # first column position of value in row 3

    cdef int f_row_col = indices_view[f_row] # first value of column in row with value
    cdef int s_row_col = indices_view[s_row] # first column in row with value
    cdef int t_row_col = indptr_view[p_index+1]
    cdef int f_row_col_start = indptr_view[a_index]
    cdef int f_row_col_stop = indptr_view[a_index+1]
    
    cdef int s_row_col_start = indptr_view[p_index]
    cdef int s_row_col_stop = indptr_view[p_index+1]

    for x in range(f_row_col_start, f_row_col_stop):
        for y in range(s_row_col_start, s_row_col_stop):
            if indices_view[x] == indices_view[y]:
                M_11 +=1
                break

    M_01_and_M_10 = ((f_row_col_stop - f_row_col_start) + (s_row_col_stop - s_row_col_start)) -(2*M_11)
    if M_01_and_M_10 < 0:
        M_01_and_M_10 = -M_01_and_M_10
  
    jaccard_index = (M_11)/ float((M_01_and_M_10 + M_11))
    jaccard_distance = 1-jaccard_index
     
    #distance_matrix[a_index, p_index] = jaccard_distance
    #distance_matrix[p_index, a_index] = jaccard_distance
    return jaccard_distance

def region_query(int p_index, float eps):
    """ compute distance for every row other than X(index)
        if distance < eps, keep neighbour as index
    """
    cdef np.ndarray[DTYPE_t, ndim=1] neighbor_indexes = np.empty(num_rows, dtype=DTYPE)
    neighbor_indexes.fill(-1)

    cdef int i = 0
    cdef float distance = 0.0

    for i in range(0, num_rows):
        if (i == p_index):
            continue
        #if (distance_matrix[p_index, i] != -1):
        #    distance = distance_matrix[p_index, i]
        #elif (distance_matrix[i, p_index] != -1):
        #    distance = distance_matrix[i, p_index]
        #else:
        distance = compute_jaccard_distance(i, p_index)
        if distance <= eps:
            neighbor_indexes[i] = 1

    return np.where(neighbor_indexes != -1)[0]

#cProfile.runctx("run_program()", globals(), locals(), "Profile.prof")

#s = pstats.Stats("Profile.prof")
#s.strip_dirs().sort_stats("tottime").print_stats()

print(timeit.timeit(run_program, number=1))
if (FILENAME == "data_100points_100dims.dat"):
    assert (np.array([ 1,  2, -1,  3,  4, -1,  4,  4, -1,  4, -1,  2,  2,  1, -1,  1,  1,  4,
     -1,  1,  2,  1,  1,  4, -1, -1,  2,  2,  1,  4,  4,  4,  4,  1, -1, -1,
      2,  1, -1,  4,  1, -1,  2,  1,  1,  4,  4,  4,  4,  1,  2,  4,  2,  4,
    -1,  1,  4, -1,  3, -1, -1,  1, -1, -1,  4, -1,  2,  2,  3,  5,  1, -1,
      1,  4, -1,  2,  2,  4, -1, -1,  1,  4, -1, -1,  5,  2,  2,  1, -1,  1,
     -1,  1, -1,  1, -1,  2,  1, -1,  2,  2,]) == cluster_indexes).all()
