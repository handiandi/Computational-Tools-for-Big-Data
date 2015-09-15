import timeit

def cpython_compute_sum(int terms = 10000):
	cdef int i, sum = 0
	for i in range(1, terms+1):
		sum += 1/(i**2)
	return sum

print(timeit.timeit(cpython_compute_sum, number=500))
