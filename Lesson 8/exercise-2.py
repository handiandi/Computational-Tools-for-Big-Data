#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mrjob.job import MRJob
from mrjob.step import MRStep

class HasEulerTour(MRJob):
	def mapper(self, key, value):
		from_edge, to_edge = value.split()
		yield((from_edge,1))
		yield((to_edge,1))

	def reducer(self, key, values):
		yield("Has Euler Tour", sum(values))
	
	def reducer2(self, key, values):
		yield(key, all([value % 2 == 0 for value in values]))
	
	def steps(self):
		return [
		MRStep(mapper=self.mapper, reducer=self.reducer),
		MRStep(reducer=self.reducer2)
		]

if __name__ == '__main__':
	HasEulerTour.run()