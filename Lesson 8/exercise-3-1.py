#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Use for the examples from slides

from mrjob.job import MRJob
from mrjob.step import MRStep

class FindCommonFriends(MRJob):
	
	def mapper(self, _, value):
		values = value.split()
		from_edge = values[0]
		for value in values[1:]:
			key = sorted([from_edge,value])
			yield(key,values[1:])

	def reducer(self, key, values):
		first_group, second_group = values
		# yield key and intersection
		yield(key, [x for x in first_group if x in second_group])

if __name__ == '__main__':
	FindCommonFriends.run()