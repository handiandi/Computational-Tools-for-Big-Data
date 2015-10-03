#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import pymongo
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
cur.execute("""SELECT DISTINCT Orders.CustomerID from Orders
			   INNER JOIN Customers on Orders.CustomerID = Customers.CustomerID 
			   INNER JOIN 'Order Details' on Orders.OrderID = 'Order Details'.OrderID 
			   INNER JOIN Products on 'Order Details'.ProductID = Products.ProductID  
			   WHERE Products.ProductID = 7 GROUP BY Orders.CustomerID""")
# produce a list of values instead of a list of single-tuples
customer_ids = [customer_id[0] for customer_id in cur.fetchall()]
placeholder = "?"
placeholders = ",".join(placeholder*len(customer_ids))

cur.execute(""" SELECT DISTINCT Products.ProductName from Products
				INNER JOIN 'Order Details' on Products.ProductID = 'Order Details'.ProductID
				INNER JOIN Orders on 'Order Details'.OrderID = Orders.OrderID
				INNER JOIN Customers on Orders.CustomerID = Customers.CustomerID WHERE Customers.CustomerID IN (%s)""" % placeholders, customer_ids)
products = [product[0] for product in cur.fetchall()]
print("Sqlite: {} different products have been purchased by Uncle Bob's Organic Dried Pears Customers\nThese are:".format(len(products)))
print("\n".join(products))
print("\n")
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
for customer in customer_ids_list:
	for order in order_collection.find({"CustomerID":customer}):
		for detail in order_details_collection.find({"OrderID":order["OrderID"]}):
			products.append(products_collection.find_one({"ProductID":detail["ProductID"]})["ProductName"])
print("MongoDB: {} different products have been purchased by Uncle Bob's Organic Dried Pears Customers\nThese are:".format(len(set(products))))
print("\n".join(set(products)))

