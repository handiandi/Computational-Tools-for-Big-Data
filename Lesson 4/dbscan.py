import pickle
import os
import numpy as np

# parameters
FILENAME = "data_10points_10dims.dat"

EPS = 0.4
M = 2

with open(os.path.join("data",FILENAME)) as f:
	X = pickle.load(f)

visited_indexes = np.zeros(X.shape[0])
cluster_indexes = np.zeros(X.shape[0])

def db_scan(eps, m):
	C = 0
	for p_index, row in enumerate(X):
		if visited_indexes[p_index]:
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
	for index, point in enumerate(neighbor_points):
		if not visited_indexes[index]:
			visited_indexes[index] = 1
			neighbor_points_prime = region_query(index, eps)
			if neighbor_points_prime.size >= m:
				np.append(neighbor_points, neighbor_points_prime)
		if cluster_indexes[index] <= 0:
			cluster_indexes[index] = C


def compute_jaccard_distance(A, B):
	M_11 = np.sum(np.logical_and(A.todense(), B.todense()))
	
	M_01_and_M_10 = np.sum(np.logical_xor(A.todense(), B.todense()))

	jaccard_index = (M_11)/ float((M_01_and_M_10 + M_11))
	jaccard_distance = 1 - jaccard_index
	return jaccard_distance

def region_query(p_index, eps):
	""" compute distance for every row other than X(index)
		if distance < eps, keep neighbour as index
	"""
	neighbor_indexes = np.zeros(X.shape[0])
	for index, row in enumerate(X):
		distance = compute_jaccard_distance(row, X[p_index,:])
		if distance <= eps:
			neighbor_indexes[index] = 1
	# why does it return tuple, fix this
	return neighbor_indexes.nonzero()[0]

db_scan(EPS, M)

print(cluster_indexes)