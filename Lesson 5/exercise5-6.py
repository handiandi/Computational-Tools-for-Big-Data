#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import pymongo
import collections
"""
Exercise 5.5
Sqlite version of exercise:
We first find the distinct customer ids of the people who've purchased Pears using the DISTINCT and procede just like in the former exercise.
Next we find all the orders orders of the customers by joining with orders, then order details joining with order details and products joining with products.
We then find the distinct products by joining the beforementioned tables again and
build a string for use with the IN keyword specifying all the customer id's whose products we are interested in.
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
				GROUP BY Products.ProductName ORDER BY No_orders DESC""")
# produce a list of values instead of a list of single-tuples
result = cur.fetchall() #[customer_id[0] for customer_id in cur.fetchall()]
result.sort(key=lambda tup: tup[0], reverse=True)  

print("Sqlite: {} is most purchased with {} purchases".format(result[0][1],result[0][0]))

con.close()

""" MongoDB version of exercise:
We first find the customers who purchased pears like in the last exercise
Next we find all the Orders and Order Details and their corresponding Products
We can then convert the list to a set to find the unique products and how many there is
"""
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
	print("{} was bought {} times".format(item, freq))

