#!/usr/bin/env python3
import json
# first we open the json-encoded pizza train file and load it into a list of dictionaries
with open("pizza-train.json") as f:
	json_string = f.read()

dicts = json.loads(json_string)

# we use a list comprehension to extract each request_text and split it using str split
# a regex could also be used using the re library
text_lists = [dictionary["request_text"].split() for dictionary in dicts]
# flatten and set it to only get distinct words, in our case we get 25083 words
distinct_words = set([word for text in text_lists for word in text])
# print each text as a bag of words count
# if we'd want to see which words belong to which column we'd have to list the distinct words as a set is not ordered
for text in text_lists:
	print(" ".join([str(text.count(word)) for word in distinct_words]))