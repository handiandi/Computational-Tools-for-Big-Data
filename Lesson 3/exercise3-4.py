#!/usr/bin/env python3
import json
import re
import sklearn
import sklearn.feature_extraction
import sklearn.linear_model
import sklearn.cross_validation
import numpy as np

# first we open the json-encoded pizza train file and load it into a list of dictionaries
with open("pizza-train.json") as f:
	dicts = json.loads(f.read())

# we use a list comprehension to extract each request_text and requester_received_pizza and put them into separate lists
text_list, received_pizza_list = zip(*[(dictionary["request_text"], dictionary["requester_received_pizza"]) for dictionary in dicts])

# instead of manually creating a bag of words like last week we can use scikit learns CountVectorizer to do the work for us
vectorizer = sklearn.feature_extraction.text.CountVectorizer()

# we fit the vectorizer and it returns the bag of words and convert the received pizza list to an np array
X = vectorizer.fit_transform(text_list).toarray()
y = np.array(received_pizza_list)

# we use sklearns Logistic Regression model and divide our dataset into train and test sets (90-10)
logistic = sklearn.linear_model.LogisticRegression()
X_train, X_test, y_train, y_test = sklearn.cross_validation.train_test_split(X, y, test_size=0.1, random_state=0)

# we fit the classifier with our test data
logistic.fit(X_train, y_train)

# we can use score to get the mean accuracy = ~0.68
print(logistic.score(X_test, y_test))

# if we want we can extract more features into our dataset like:
# number of posts on the subreddit at retrieval, which perhaps can be correlated with a request being fulfilled
num_upvotes = np.array([[dictionary["requester_number_of_posts_on_raop_at_retrieval"]] for dictionary in dicts])

X = np.append(X, num_upvotes, axis=1)

logistic = sklearn.linear_model.LogisticRegression()
X_train, X_test, y_train, y_test = sklearn.cross_validation.train_test_split(X, y, test_size=0.1, random_state=0)

# we fit the classifier with our test data
logistic.fit(X_train, y_train)

# then we get a mean accuracy = ~0.77
print(logistic.score(X_test, y_test))