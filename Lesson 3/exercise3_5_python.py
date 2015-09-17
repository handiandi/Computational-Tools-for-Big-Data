#!/usr/bin/env python3
import timeit

def python_compute_sum(terms=10000):
	sum = 0
	for i in range(1, terms+1):
		sum += 1/(i**2)
	return sum
# execution time on a i5 2500k = 1.1080237 
print(timeit.timeit(python_compute_sum, number=500))
