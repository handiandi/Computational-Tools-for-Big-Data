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
import sys

DTYPE = np.int
DTYPE_FLOAT = np.float
ctypedef np.int_t DTYPE_t
ctypedef np.float_t DTYPE_FLOAT_t

    # parameters
FILENAME = "data_100points_100dims.dat"
cdef float EPS = 0.3
cdef int M = 2

file_handler = open(os.path.join("data",FILENAME),"rb")
X = pickle.load(file_handler, encoding="latin1")
# print(X.todense())
# print("X.data: \n")
# print(X.data)
# print("X.indices: \n")
# print(X.indices)
# print("X.indptr:")
# print(X.indptr)

file_handler.close()

cdef int [:] indices_view = X.indices.astype(np.dtype("i"))

cdef int [:] indptr_view = X.indptr.astype(np.dtype("i"))

cdef float [:] data_view = X.data.astype(np.dtype("f"))

cdef int num_rows = X.get_shape()[0]
cdef int num_cols = X.get_shape()[1]
distance_matrix_np = np.empty((num_rows,num_cols), dtype=np.dtype("double"))
distance_matrix_np.fill(-1)
cdef double [:,:] distance_matrix = distance_matrix_np

cdef int [:] visited_indexes = np.zeros(num_rows, dtype=np.dtype("i"))
cdef int [:] cluster_indexes = np.zeros(num_rows, dtype=np.dtype("i"))

def run_program():
    db_scan(EPS, M)

    print(np.array(cluster_indexes))
    print(np.unique(cluster_indexes).size)

def db_scan(float eps, int m):
    cdef int p_index, C = 0
    cdef int num_rows = distance_matrix.shape[0]
    for p_index in range(0, num_rows):
        # check if visited or already in cluster
        if visited_indexes[p_index]:
            continue
        visited_indexes[p_index] = 1
        neighbor_points = region_query(p_index, eps)
        if neighbor_points.size < m-1:
            cluster_indexes[p_index] = -1
        else:
            C += 1
            expand_cluster(p_index, neighbor_points, C, eps, m)

def expand_cluster(int p_index, np.ndarray[DTYPE_t, ndim=1] neighbor_points, int C, float eps, int m):
    cluster_indexes[p_index] = C
    cdef int i = 0
    cdef int index = 0
    while i < neighbor_points.size:
        index = neighbor_points[i]
        if not visited_indexes[index]:
            visited_indexes[index] = 1
            neighbor_points_prime = region_query(index, eps)
            if neighbor_points_prime.size >= m-1:
                neighbor_points = np.append(neighbor_points, neighbor_points_prime)
        if cluster_indexes[index] == 0:
            cluster_indexes[index] = C
        i += 1

def compute_jaccard_distance(int a_index, int [:] p_index_row, int p_index):
    cdef int M_11, M_01_and_M_10
    cdef float jaccard_index, jaccard_distance

    #cdef int [:] X_a_index_row = extract_row(a_index)
    #cdef int [:] X_b_index_row = extract_row(b_index)



    cdef int f_row = indptr_view[a_index] #første kolonne-potition af en værdi i række 1 
    cdef int s_row = indptr_view[p_index] #første kolonne-potition af en værdi i række 2
    cdef int t_row = indptr_view[p_index+1] #første kolonne-potition af en værdi i række 3

    cdef int f_row_col = indices_view[f_row] #første værdi i kollonne i række med værdi
    cdef int s_row_col = indices_view[s_row] #første kollonne i række med værdi
    cdef int t_row_col = indptr_view[p_index+1]
    #f_row_col_start = indptr_view[a_index]
    #f_row_col_stop = indptr_view[a_index+1]

    #print("før loop: f_row = {0}".format(f_row))
    #print("før loop: f_row_col = {0}".format(f_row_col))
    #print("før loop: f_row = {0}".format(f_row))
    #print("før loop: s_row_col = {0}".format(s_row_col))
    cdef int f_row_col_start = indptr_view[a_index]
    cdef int f_row_col_stop = indptr_view[a_index+1]
    

    #f_row_col_start = indptr_view[a_index]
    #f_row_col_stop = indptr_view[a_index+1]
    cdef int s_row_col_start = indptr_view[p_index]
    cdef int s_row_col_stop = indptr_view[p_index+1]
    cdef int temp = -1

    # for i in range(0, num_rows):
    #     #print("f_row_col: {0}".format(f_row_col))
    #     #print("indices_view[f_row+i]: {0}".format(indices_view[f_row+i]))
    #     if i == 0:
    #         temp = indices_view[f_row+i]
    #         continue
    #     elif indices_view[f_row+i] <= temp:
    #         f_row_col_stop = ((f_row+i)-1)
    #         break
    #     else:
    #         temp = indices_view[f_row+i]

    #print("For {0} og {1}:\n".format(a_index, p_index))
    # print("f_start = {0} \n".format(f_row_col_start))
    # print("f_stop = {0} \n\n".format(f_row_col_stop))
    # #sys.exit("Error message")

    # temp = -1
    # for i in range(0, num_rows):
    #     if i == 0:
    #         temp = indices_view[s_row+i]
    #         continue
    #     if indices_view[s_row+i]<=temp:
    #         s_row_col_stop = ((s_row+i)-1)
    #         break
    #     else:
    #         temp= indices_view[s_row+i]

    # print("s_start = {0} \n".format(s_row_col_start))
    # print("s_stop = {0} ".format(s_row_col_stop))
    
    #sys.exit("Error message")

    M_11 = 0
    M_01_and_M_10 = 0
    flag = 0


    for x in range(f_row_col_start, f_row_col_stop):
        for y in range(s_row_col_start, s_row_col_stop):
            if indices_view[x] == indices_view[y]:
                flag = 1
                break
        if flag == 1:
            M_11 +=1
            flag = 0

    
    
    M_01_and_M_10 = ((f_row_col_stop - f_row_col_start) + (s_row_col_stop - s_row_col_start)) -(2*M_11)
    if M_01_and_M_10 < 0:
        M_01_and_M_10 = -M_01_and_M_10

    #print("11 = {0}\n0110 = {1}\n".format(M_11, M_01_and_M_10))
    #print("{0}\n{1}\n-----".format(np.array(indices_view[f_row_col_start:f_row_col_stop]), np.array(indices_view[s_row_col_start:s_row_col_stop])))
    jaccard_index = (M_11)/ float((M_01_and_M_10 + M_11))
    jaccard_distance = 1-jaccard_index
    #print("jaccard_distance = {0}\n\n--------------------\n".format(jaccard_distance))
    #sys.exit("Error message")
    #for i in range(0,num_rows):
    #    if X_a_index_row[i] == 1 and X_a_index_row[i] == p_index_row[i]:
    #        M_11 += 1
    #    elif X_a_index_row[i] != p_index_row[i]:
    #        M_01_and_M_10 +=1

    #jaccard_index = (M_11)/ float((M_01_and_M_10 + M_11))
    #jaccard_distance = 1-jaccard_index
    
    distance_matrix[a_index, p_index] = jaccard_distance
    distance_matrix[p_index, a_index] = jaccard_distance
    return jaccard_distance

def extract_row(int i):
    cdef int[:] row_list = np.empty(num_rows, dtype=np.dtype("i"))

    cdef int current_index = 0
    cdef int zero_index = 0
    cdef int j

    for i in range(indptr_view[i], indptr_view[i+1]):
        j = indices_view[i]
        while(zero_index < j):
            row_list[current_index] = 0
            current_index += 1
            zero_index += 1
        row_list[current_index] = 1
        current_index += 1
        zero_index += 1
    while(zero_index < num_rows):
        row_list[current_index] = 0
        current_index += 1
        zero_index += 1
    return row_list

def region_query(int p_index, float eps):
    """ compute distance for every row other than X(index)
        if distance < eps, keep neighbour as index
    """
    cdef np.ndarray[DTYPE_t, ndim=1] neighbor_indexes = np.empty(distance_matrix.shape[0], dtype=DTYPE)
    neighbor_indexes.fill(-1)
    cdef int i = 0
    cdef float distance = 0.0
    cdef int num_rows = distance_matrix.shape[0]

    cdef int [:] p_index_row = extract_row(p_index)
    for i in range(0, num_rows):
        if (i == p_index):
            continue
        if (distance_matrix[p_index, i] != -1):
            distance = distance_matrix[p_index, i]
        elif (distance_matrix[i, p_index] != -1):
            distance = distance_matrix[i, p_index]
        else:
            distance = compute_jaccard_distance(i, p_index_row, p_index)
        if distance <= eps:
            neighbor_indexes[i] = 1
    # why does it return tuple, fix this
    return np.where(neighbor_indexes != -1)[0]

cProfile.runctx("run_program()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("tottime").print_stats()

#print(timeit.timeit(run_program, number=1))

assert (np.array([ 1,  2, -1,  3,  4, -1,  4,  4, -1,  4, -1,  2,  2,  1, -1,  1,  1,  4,
 -1,  1,  2,  1,  1,  4, -1, -1,  2,  2,  1,  4,  4,  4,  4,  1, -1, -1,
  2,  1, -1,  4,  1, -1,  2,  1,  1,  4,  4,  4,  4,  1,  2,  4,  2,  4,
 -1,  1,  4, -1,  3, -1, -1,  1, -1, -1,  4, -1,  2,  2,  3,  5,  1, -1,
  1,  4, -1,  2,  2,  4, -1, -1,  1,  4, -1, -1,  5,  2,  2,  1, -1,  1,
 -1,  1, -1,  1, -1,  2,  1, -1,  2,  2,]) == cluster_indexes).all()