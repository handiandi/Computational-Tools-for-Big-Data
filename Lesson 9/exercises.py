
# coding: utf-8

# ### Exercise 1

# ####Write a Spark job to count the occurrences of each word in a text file. Document that it works with a small example.

# In[17]:

lines = sc.textFile("exercise1_data.txt") #Extracting the lines in the file

words = lines.flatMap(lambda s: s.split()) #Splitting the lines into words
pairs = words.map(lambda s: (s, 1)) #Creating a pair for each word in the form (word, count) where count is the occurrence of the word, set to 1
counts = pairs.reduceByKey(lambda a, b: a + b) #Counting the words

res = sorted(counts.collect(), key=lambda tup: tup[1], reverse=True) #Get the result and sort it based on count
for (word, count) in res:
    print("'{0}' has an occurrences of {1}".format(word,count)) #Print out the result


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


# ### Exercise 3

# In[27]:

wifi_data = sc.textFile("wifi.data")


# ####What are the 10 networks I observed the most, and how many times were they observed? Note: the bssid is unique for every network, the name (ssid) of the network is not necessarily unique.

# In[87]:

# convert each row to a dict and extract bssid
bssids = wifi_data.map(lambda e: eval(e)["bssid"])
# convert each row to a bssid,1 tuple
bssid_pairs = bssids.map(lambda l: (l,1))
# reduce by key by adding a 1 for each bssid
bssid_counts = bssid_pairs.reduceByKey(lambda a, b: a + b)
# get 10 bssids sorted by descending count
bssid_counts.takeOrdered(10, key=lambda x: -x[1])


# ####What are the 10 most common wifi names? (ssid)

# In[82]:

wifi_dicts = wifi_data.map(lambda e: eval(e))
# get distinct ssid, bssid pairs
ssid_bssid_pairs = wifi_dicts.map(lambda l: (l["ssid"],l["bssid"])).distinct()
# get counts of ssids
ssid_tuples = ssid_bssid_pairs.map(lambda l: (l[0],1))
ssid_counts = ssid_tuples.reduceByKey(lambda a, b: a + b)
ssid_counts.takeOrdered(10, key=lambda x: -x[1])


# ####What are the 10 longest wifi names? (again, ssid)

# In[85]:

# convert each entry to a dict and get the distinct ssids
ssids = wifi_data.map(lambda e: eval(e)["ssid"]).distinct()
# take 10 and order descending
ssids.takeOrdered(10, key=lambda x: -len(x))


# In[ ]:



