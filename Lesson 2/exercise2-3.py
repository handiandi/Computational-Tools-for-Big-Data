#!/usr/bin/env python3
import json
import re
import sys
# we can either get filename as an arg or just use the pizza-train.json file
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = "pizza-train.json"

# first we open the json-encoded pizza train file and load it into a list of dictionaries
with open(file_name) as f:
	dicts = json.loads(f.read())

# we use a list comprehension to extract each request_text and split it using a regex generating a list of lists
text_lists = [re.split("\W+",dictionary["request_text"]) for dictionary in dicts]

# flatten and set it to only get distinct words, in our case we get 14899 words
distinct_words = set([word for text in text_lists for word in text])

# create matrix with each text as a bag of words count
# if we'd want to see which words belong to which column we'd have to list the distinct words as a set is not ordered
matrix = []
for text in text_lists:
	matrix.append([text.count(word) for word in distinct_words])
for row in matrix:
   print(row)
