#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import exercise_11_1
import random
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

articles = exercise_11_1.preprocess_texts()
articles = articles[:100]

# binary bag of words matrix with the tokenizer we defined in exercise 11-1
vectorizer = CountVectorizer(tokenizer=exercise_11_1.tokenizer, binary=True)

X = vectorizer.fit_transform([article["body"] for article in articles]).toarray()

NUMBER_OF_PERMUTATIONS = 10

X_mod = np.empty(([X.shape[0],NUMBER_OF_PERMUTATIONS]), dtype=int)
print(X_mod.shape)		

for i in range(NUMBER_OF_PERMUTATIONS):
	seed = random.random()
	for index, row in enumerate(X):
		current = np.copy(row)
		random.shuffle(current, lambda: seed)
		X_mod[index,i] = np.where(current == 1)[0][0]

group_dictionary = {}

for index, row in enumerate(X_mod):
	tupled = tuple(row)
	if tupled not in group_dictionary:
		group_dictionary[tupled] = []
	group_dictionary[tupled].append(index)

for key, indexes in group_dictionary.items():
	print(len(indexes))
