# ### Exercise 3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Exercise 3
wifi_data = sc.textFile("wifi.data")


# ####What are the 10 networks I observed the most, and how many times were they observed? Note: the bssid is unique for every network, the name (ssid) of the network is not necessarily unique.

# convert each row to a dict and extract bssid
bssids = wifi_data.map(lambda e: eval(e)["bssid"])
# convert each row to a bssid,1 tuple
bssid_pairs = bssids.map(lambda l: (l,1))
# reduce by key by adding a 1 for each bssid
bssid_counts = bssid_pairs.reduceByKey(lambda a, b: a + b)
# get 10 bssids sorted by descending count
bssid_counts.takeOrdered(10, key=lambda x: -x[1])


# ####What are the 10 most common wifi names? (ssid)

wifi_dicts = wifi_data.map(lambda e: eval(e))
# get distinct ssid, bssid pairs
ssid_bssid_pairs = wifi_dicts.map(lambda l: (l["ssid"],l["bssid"])).distinct()
# get counts of ssids
ssid_tuples = ssid_bssid_pairs.map(lambda l: (l[0],1))
ssid_counts = ssid_tuples.reduceByKey(lambda a, b: a + b)
ssid_counts.takeOrdered(10, key=lambda x: -x[1])


# ####What are the 10 longest wifi names? (again, ssid)

# convert each entry to a dict and get the distinct ssids
ssids = wifi_data.map(lambda e: eval(e)["ssid"]).distinct()
# take 10 and order descending
ssids.takeOrdered(10, key=lambda x: -len(x))