#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import exercise_11_1
import random
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
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
	NUMBER_OF_PERMUTATIONS = 10

	# get 100 articles
	articles = sorted(exercise_11_1.preprocess_texts(), key=lambda k: k['id'])
	 #gets all articles and sort it by id key
	SEED = 448
	random.seed(SEED)
	random.shuffle(articles) #Shuffle the articles based on a seed
	random.seed()
	articles = articles[:100] #take the first 100 articles
	# create binary bag of words matrix with the tokenizer we defined in exercise 11-1
	X = exercise_11_1.create_bow(articles, exercise_11_1.tokenizer, True).toarray()

	# create minhashed representation with a number of permutations
	X_mod = create_minhashed_matrix(X, NUMBER_OF_PERMUTATIONS)

	# create a dictionary of: tupled minhash representation -> list of indexes
	bucket_dict = create_bucket_dict(X_mod)

	print("#### Summary ####")
	print("There are {} buckets with the following number of articles in them:\n----------------------".format(len(bucket_dict)))
	for key, indexes in bucket_dict.items():
		print(len(indexes))
		topics = [articles[i]["topics"] for i in indexes]
		# flatten
		topics = [topic for sublist in topics for topic in sublist]
		print(Counter(topics))

	print("#################\n")
	print("#### Printing 3 random articles from buckets which have more than 3 articles ####\n----------------------")
	for key, indexes in bucket_dict.items():
		if len(indexes)>3:
			print("\n-----------------------\nBucket with {} articles in it\n-----------------------\n".format(len(indexes)))
			for index in random.sample(indexes, 3):
				print("\nXXXXXXXXXX\nNew article\nXXXXXXXXXX\n")
				print(articles[index]["body"])
				print(articles[index]["topics"])




