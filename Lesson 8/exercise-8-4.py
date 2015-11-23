#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mrjob.job import MRJob
from mrjob.step import MRStep

class FindTriangles(MRJob):
	"""
	yield two key, value which is conversed:
	From (A B) its yields (A B) and (B A)
	"""
	def convert_mapper(self, _, value):
		from_edge, to_edge = value.split()
		yield(int(from_edge),int(to_edge))
		yield(int(to_edge),int(from_edge))

	"""
	Collects all values for that key
	"""
	def convert_reducer(self, key, values):
		yield(key, tuple(values))
	
	"""
	For every values it yields a new key, 
	which is a list of the old key and the value
	"""
	def main_mapper(self, key, values):
		for value in values:
			new_key = sorted([key,value])
			yield(new_key,values)

	"""
	Its finds common "friends" (nodes) of its key-values
	The new key is the original key and the new friend
	It yields the new and the value 1
	"""
	def main_reducer(self, key, values):
		first_group, second_group = values
		res = [x for x in first_group if x in second_group]
		for value in res:
			new_key = key[:]
			new_key.append(value)
			new_key = sorted(new_key)
			yield(new_key,1)

	"""
	Its reduce by key and sums the value and yields this
	"""
	def sum_reducer(self, key, values):
		yield(key, sum(values))

	"""
	If both the length of key and value is 3, 
	then it is a triangle and it yields 1 with the key 
	"Number of Triangles"
	If not, it yields the same key but with the value 0
	"""
	def count_triangle_mapper(self, key, value):
		n = 0
		if len(key) == 3 and value == 3:
			n = 1
		yield("Number of Triangles", n)

	"""
	It sums the triangles
	"""
	def sum_triangle_reducer(self, key, values):
		yield(key, sum(values))

	def steps(self):
		return [
		MRStep(mapper=self.convert_mapper, reducer=self.convert_reducer),
		MRStep(mapper=self.main_mapper, reducer=self.main_reducer),
		MRStep(reducer=self.sum_reducer),
		MRStep(mapper=self.count_triangle_mapper, reducer=self.sum_triangle_reducer) 
		]

if __name__ == '__main__':
	FindTriangles.run()
	