#!/usr/bin/env python3
import json
import re

# first we open the json-encoded pizza train file and load it into a list of dictionaries
with open("pizza-train.json") as f:
	dicts = json.loads(f.read())

# we use a list comprehension to extract each request_text and split it using a regex generating a list of lists
text_lists = [re.split("\W+",dictionary["request_text"]) for dictionary in dicts]

# flatten and set it to only get distinct words, in our case we get 14899 words
distinct_words = set([word for text in text_lists for word in text])

# print each text as a bag of words count
# if we'd want to see which words belong to which column we'd have to list the distinct words as a set is not ordered
for text in text_lists:
	print(" ".join([str(text.count(word)) for word in distinct_words]))