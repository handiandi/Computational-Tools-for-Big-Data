#!/usr/bin/env python3

def load_array(path):
	multi_array = []
	with open(path) as f:
		for line in f:
			multi_array.append(line.split())
	return multi_array

def save_array(multi_array, path="saved_array.txt"):
	with open(path,"w+") as f:
		for array in multi_array:
			# could also use a list comprehension
			f.write(" ".join(map(str, array))+"\n")


print(load_array("array.txt"))
save_array([[1,2,3],[4,5,6],[7,8,9]])