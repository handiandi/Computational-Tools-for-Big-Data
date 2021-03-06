#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mmh3
import bitarray
import math
import re
import timeit
from nltk.stem.snowball import SnowballStemmer

class BloomFilter():
	def __init__(self, num_bits, estimated_distinct):
		self.num_bits = num_bits
		self.array = bitarray.bitarray(num_bits)
		self.array.setall(0)
		self.hash_seeds = range(math.ceil(num_bits/estimated_distinct * math.log(2)))
	
	def add(self, string):
		for seed in self.hash_seeds:
			index = mmh3.hash(string, seed=seed) % self.num_bits
			self.array[index] = 1
	
	def lookup(self, string):
		for seed in self.hash_seeds:
			index = mmh3.hash(string, seed=seed) % self.num_bits
			if self.array[index] == 0:
				return False
		return True
"""
Helper function for processing a string into words
"""
def extract_text(string):
	lowered = string.lower().strip()
	words = re.split("\W+", lowered)
	stemmer = SnowballStemmer("english")
	return [stemmer.stem(word) for word in words]

def bloom_filter_main():
	NUM_BITS = 1000000
	# number of words in dictionary
	ESTIMATED_DISTINCT = 235887
	not_found_list = []

	b_filter = BloomFilter(NUM_BITS, ESTIMATED_DISTINCT)
	stemmer = SnowballStemmer("english")
	with open("dict.txt") as f:
		for line in f:
			b_filter.add(stemmer.stem(line.strip()))
	with open("shakespeare.txt") as f:
		for line in f:
			line_words = extract_text(line)
			for word in line_words:
				found = b_filter.lookup(word)
				if not found:
					not_found_list.append(word)
	return not_found_list

def non_bloom_filter_main():
	not_found_list = []

	with open("dict.txt") as dict_file:
		stemmer = SnowballStemmer("english")
		dict_words = dict_file.read().splitlines()
		dict_words = [stemmer.stem(word) for word in dict_words]

	with open("shakespeare.txt") as f:
		shakespeare_words = extract_text(f.read())
	
	for word in shakespeare_words:
		found = False
		for entry in dict_words:
			if word == entry:
				found = True
				break
		if not found:
			not_found_list.append(word)
	return not_found_list

if __name__ == '__main__':
	print(timeit.timeit(bloom_filter_main, number=1))
	print(timeit.timeit(non_bloom_filter_main, number=1))

	bloom_filter_list = bloom_filter_main()
	non_bloom_filter_list = non_bloom_filter_main()
	print("{} words not in dictionary (in non bloom filter set) and {} words not in dictionary (in bloom filter set), thus a false positive rate of {}".format(len(set(non_bloom_filter_list)),len(set(bloom_filter_list)),1-(len(set(bloom_filter_list))/len(set(non_bloom_filter_list)))))
	print("words not in dictionary but reported to be:")
	for string in set(non_bloom_filter_list)-set(bloom_filter_list):
		print(string)

