#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):
	def mapper(self, key,value):
		for word in value.split():
			yield word, 1

	def reducer(self,key,value):
		yield key, sum(value)



if __name__ == '__main__':
    MRWordFrequencyCount.run()