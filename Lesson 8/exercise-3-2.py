#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Use for the Facebook file

from mrjob.job import MRJob
from mrjob.step import MRStep

class FindCommonFriends(MRJob):
	def convert_mapper(self, _, value):
		from_edge, to_edge = value.split()
		yield(int(from_edge),int(to_edge))
		yield(int(to_edge),int(from_edge))

	def convert_reducer(self, key, values):
		yield(key, tuple(values))
	
	def main_mapper(self, key, values):
		for value in values:
			new_key = sorted([key,value])
			yield(new_key,values)

	def main_reducer(self, key, values):
		first_group, second_group = values
		# yield key and intersection
		yield(key, [x for x in first_group if x in second_group])
	
	def steps(self):
		return [
		MRStep(mapper=self.convert_mapper, reducer=self.convert_reducer),
		MRStep(mapper=self.main_mapper, reducer=self.main_reducer)
		]

if __name__ == '__main__':
	FindCommonFriends.run()