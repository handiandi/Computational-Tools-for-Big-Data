#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import exercise_11_1
import random
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def create_bucket_dict(X):
	bucket_dict = {}
	for index, row in enumerate(X):
		bucket_key = tuple(row)
		if bucket_key not in bucket_dict:
			bucket_dict[bucket_key] = []
		bucket_dict[bucket_key].append(index)
	return bucket_dict

def create_minhashed_matrix(X, permutations):
	X_mod = np.empty(([X.shape[0],NUMBER_OF_PERMUTATIONS]), dtype=int)
	for i in range(permutations):
		seed = random.random()
		for index, row in enumerate(X):
			current = np.copy(row)
			random.shuffle(current, lambda: seed)
			X_mod[index,i] = np.where(current == 1)[0][0]
	return X_mod


if __name__ == '__main__':
	NUMBER_OF_PERMUTATIONS = 20

	# get 100 articles
	articles = exercise_11_1.preprocess_texts()
	articles.sort(key=lambda a: a["id"])
	random.seed(1)
	random.shuffle(articles)
	random.seed()
	articles = articles[:100]

	# create binary bag of words matrix with the tokenizer we defined in exercise 11-1
	X = exercise_11_1.create_bow(articles, exercise_11_1.tokenizer, True).toarray()

	# create minhashed representation with a number of permutations
	X_mod = create_minhashed_matrix(X, NUMBER_OF_PERMUTATIONS)

	# create a dictionary of: tupled minhash representation -> list of indexes
	bucket_dict = create_bucket_dict(X_mod)

	for key, indexes in bucket_dict.items():
		print(len(indexes))
	for key, indexes in bucket_dict.items():
		if len(indexes) > 1 and len(indexes) < 50:
			for index in indexes:
				print(articles[index]["body"])
				print("XXXXXXXXXX")
			print("-------------")
