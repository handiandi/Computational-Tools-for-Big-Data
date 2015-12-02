#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pyspark import SparkContext

# apache spark test job

# Write a Spark job to count the occurrences of each word in a text file. Document that it works with a small example.
CONNECTION_STR = "spark://"+os.environ["SPARK_MASTER_PORT_7077_TCP_ADDR"]+":"+os.environ["SPARK_MASTER_ENV_SPARK_MASTER_PORT"]
sc = SparkContext(CONNECTION_STR,"test")

lines = sc.textFile("exercise1_data.txt") #Extracting the lines in the file

words = lines.flatMap(lambda s: s.split()) #Splitting the lines into words
pairs = words.map(lambda s: (s, 1)) #Creating a pair for each word in the form (word, count) where count is the occurrence of the word, set to 1
counts = pairs.reduceByKey(lambda a, b: a + b) #Counting the words

res = sorted(counts.collect(), key=lambda tup: tup[1], reverse=True) #Get the result and sort it based on count
for (word, count) in res:
    print("'{0}' has an occurrences of {1}".format(word,count)) #Print out the result
