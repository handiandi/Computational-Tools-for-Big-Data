#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sklearn
import mmh3
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(SCRIPT_DIR, "reuters-articles")
ARTICLE_FILENAMES = [filenames for (_, _, filenames) in os.walk(ARTICLES_DIR)][0]

def is_valid_article(article):
	if not "topics" in article:
		return False
	if not len(article["topics"]) > 0:
		return False
	if not "body" in article:
		return False
	if not len(article["body"]) > 0:
		return False
	return True

def preprocess_texts():
	articles = []
	for filename in ARTICLE_FILENAMES:
		with open(os.path.join(ARTICLES_DIR, filename)) as f:
			articles.extend(json.load(f))
	# filter texts without topics or body
	articles = [a for a in articles if is_valid_article(a)]
	return articles

def hashing_vectorizer(article_words, num_buckets):
	x = np.zeros(num_buckets, dtype=int)
	for word in article_words:
		x[mmh3.hash(word) % NUM_BUCKETS] += 1
	return x

def tokenizer(article_body):
	return [word.lower() for word in article_body.split()]

def bow_trainer(articles):
	vectorizer = CountVectorizer(tokenizer=tokenizer)
	X = vectorizer.fit_transform([article["body"] for article in articles])
	y = ["earn" in article["topics"] for article in articles]
	print(X.shape)

	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
	random_forest = RandomForestClassifier(n_estimators=50)
	random_forest.fit(X_train, y_train)
	print(random_forest.score(X_test, y_test))

def hash_trainer(articles, num_buckets):
	num_articles = len(articles)

	X = np.empty((num_articles,num_buckets), dtype=np.ndarray)

	for i in range(num_articles):
		X[i] = hashing_vectorizer(tokenizer(articles[i]["body"]), num_buckets)
	y = np.array(["earn" in article["topics"] for article in articles])
	print(X.shape)

	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
	random_forest = RandomForestClassifier(n_estimators=50)
	random_forest.fit(X_train, y_train)
	print(random_forest.score(X_test, y_test))

if __name__ == '__main__':
	NUM_BUCKETS = 1000
	# 3776 of 10377 has earn topic
	articles = preprocess_texts()

	bow_trainer(articles)
	hash_trainer(articles,NUM_BUCKETS)
