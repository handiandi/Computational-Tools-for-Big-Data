#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import pymongo
import collections
"""
Exercise 5.6
Sqlite version of exercise:
Inner SELECT of the query:
We first find the distinct customer ids of the people who've purchased Uncle Bob using the DISTINCT.

Outer SELECT of the query:
We find all ProductNames and frequence of them (using count), where ProductID is not Uncle Bob and where CustomerID can be found in the result from the inner SELECT
Last, we sort by the frequence of ProductNames and limit the result to only 5. 

We print the result using a simple loop. 
"""
con = sqlite3.connect("northwind.db")
con.text_factory = lambda x: str(x, 'latin1')
cur = con.cursor()
cur.execute("""SELECT count(Products.ProductName) as No_orders, Products.ProductName from Products
				INNER JOIN 'Order Details' on Products.ProductID = 'Order Details'.ProductID
				INNER JOIN Orders on 'Order Details'.OrderID = Orders.OrderID
				INNER JOIN Customers on Orders.CustomerID = Customers.CustomerID 
				WHERE Products.ProductID != 7 AND Customers.CustomerID IN 
					(SELECT DISTINCT Orders.CustomerID from Orders
					INNER JOIN Customers on Orders.CustomerID = Customers.CustomerID 
					INNER JOIN 'Order Details' on Orders.OrderID = 'Order Details'.OrderID 
					INNER JOIN Products on 'Order Details'.ProductID = Products.ProductID  
					WHERE Products.ProductID = 7 GROUP BY Orders.CustomerID)
				GROUP BY Products.ProductName ORDER BY No_orders DESC LIMIT 5""")
# produce a list of values instead of a list of single-tuples
products = cur.fetchall() 

con.close()
print("Sqlite part:\n----------------")
for freq, item in products:
	print("{} has bought {}".format(freq, item))

""" MongoDB version of exercise:
We first find the customers who purchased Uncle Bob
Next we find all the Orders and Order Details
Then, find their corresponding Products where ProductID is not 7 (Uncle Bob)

We can then print the result (top 5)
"""
print("\nMongoDB part:\n---------------")
client = pymongo.MongoClient('localhost', 27017)
db = client["Northwind"]
customer_collection = db["customers"]
order_collection = db["orders"]
order_details_collection = db["order-details"]
products_collection = db["products"]

customer_ids_list = []
pear_details = order_details_collection.find({"ProductID":7})
for detail in pear_details:
	for order in order_collection.find({"OrderID": detail["OrderID"]}):
		customer_ids_list.append(order["CustomerID"])

products = []
for customer in set(customer_ids_list):
	for order in order_collection.find({"CustomerID":customer}):
		for detail in order_details_collection.find({"OrderID":order["OrderID"]}):
			product = (products_collection.find_one({'$and': [ {"ProductID":detail["ProductID"] }, {"ProductID": {'$ne': 7}} ] }))
			if product:
				products.append(product["ProductName"])

for item, freq in collections.Counter(products).most_common(5):
	print("{} has bought {}".format(freq, item))

