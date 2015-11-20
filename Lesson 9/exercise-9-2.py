#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Exercise 2

# #### Write a Spark job that determines if a graph has an Euler tour (all vertices have even degree) where you can assume that the graph you get is connected.

# In[12]:

def has_euler_tour(text_file_name):
    graph_data = sc.textFile(text_file_name)
    graph_data = graph_data.map(lambda a: (int(a.split()[0]),int(a.split()[1])))

    graph_tuples = graph_data.flatMap(lambda (a): [(a[0],a[1]),(a[1],a[0])] )
    graph_counts = graph_tuples.map(lambda a: (a[0],1))
    graph_counts = graph_counts.reduceByKey(lambda a, b: a + b)
    graph_even_edges = graph_counts.filter(lambda a: a[1] % 2 != 0)
    return graph_even_edges.count() == 0

graph_names = ["graph1.txt", "graph2.txt", "graph3.txt", "graph4.txt", "graph5.txt"]
for file_name in graph_names:
    print(has_euler_tour(file_name))

