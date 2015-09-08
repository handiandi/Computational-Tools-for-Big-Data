#!/usr/bin/env python3
import sys

def load_array(path):
	multi_array = []
	with open(path) as f:
		for line in f:
			multi_array.append(line.split())
	return multi_array

def save_array(path, multi_array):
	with open(path,"w+") as f:
		for array in multi_array:
			# could also use a list comprehension
			f.write(" ".join(map(str, array))+"\n")

if __name__ == "__main__":
	if len(sys.argv) != 3 or (sys.argv[1] != "load" and sys.argv[1] != "save"):
		print("exercise-2-1.py OPTION PATH")
		print("OPTION can be save or load")
		print("PATH is path to save or load to")
		sys.exit(1)

	path = sys.argv[2]

	if sys.argv[1] == "load":
		array = load_array(path)
		print(array)
	elif sys.argv[1] == "save":
		proof_of_concept_array = [[1, 2],[2, 3],[3, 4]]
		array = save_array(path, proof_of_concept_array)