#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import os
import numpy as np
import timeit

# parameters
FILENAME = "data_100points_100dims.dat"

EPS = 0.3
M = 2

with open(os.path.join("data",FILENAME),"rb") as f:
	X = pickle.load(f, encoding="latin1")

visited_indexes = np.zeros(X.shape[0])
cluster_indexes = np.zeros(X.shape[0])

def db_scan(eps, m):
	C = 0
	for p_index in np.arange(X.shape[0]):
		if visited_indexes[p_index] or cluster_indexes[p_index] != 0:
			continue
		visited_indexes[p_index] = 1
		neighbor_points = region_query(p_index, eps)
		if neighbor_points.size < m:
			cluster_indexes[p_index] = -1
		else:
			C += 1
			expand_cluster(p_index, neighbor_points, C, eps, m)

def expand_cluster(p_index, neighbor_points, C, eps, m):
	cluster_indexes[p_index] = C
	i = 0
	while i < neighbor_points.size:
		if not visited_indexes[neighbor_points[i]] or cluster_indexes[p_index] == 0:
			visited_indexes[neighbor_points[i]] = 1
			neighbor_points_prime = region_query(neighbor_points[i], eps)
			if neighbor_points_prime.size >= m:
				neighbor_points = np.append(neighbor_points, neighbor_points_prime)
		if cluster_indexes[neighbor_points[i]] == 0:
			cluster_indexes[neighbor_points[i]] = C
		i += 1

def compute_jaccard_distance(A, B):
	M_11 = (A.multiply(B)).getnnz()
	M_01_and_M_10 = np.absolute((A-B).getnnz())
	jaccard_index = (M_11)/ float((M_01_and_M_10 + M_11))
	jaccard_distance = 1 - jaccard_index
	return jaccard_distance

def region_query(p_index, eps):
	""" compute distance for every row other than X(index)
		if distance < eps, keep neighbour as index
	"""
	neighbor_indexes = np.zeros(X.shape[0])
	for i in np.arange(X.shape[0]):
		distance = compute_jaccard_distance(X.getrow(i), X.getrow(p_index))
		if distance <= eps:
			neighbor_indexes[i] = 1
	# why does it return tuple, fix this
	return neighbor_indexes.nonzero()[0]

def run_program():
	db_scan(EPS, M)
	print(cluster_indexes)
	print(np.unique(cluster_indexes).size)

print(timeit.timeit("run_program()",number=1, setup="from __main__ import run_program"))
assert (np.array([ 1,  2, -1,  3,  4, -1,  4,  4, -1,  4, -1,  2,  2,  1, -1,  1,  1,  4,
 -1,  1,  2,  1,  1,  4, -1, -1,  2,  2,  1,  4,  4,  4,  4,  1, -1, -1,
  2,  1, -1,  4,  1, -1,  2,  1,  1,  4,  4,  4,  4,  1,  2,  4,  2,  4,
 -1,  1,  4, -1,  3, -1, -1,  1, -1, -1,  4, -1,  2,  2,  3,  5,  1, -1,
  1,  4, -1,  2,  2,  4, -1, -1,  1,  4, -1, -1,  5,  2,  2,  1, -1,  1,
 -1,  1, -1,  1, -1,  2,  1, -1,  2,  2,]) == cluster_indexes).all()