#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import pymongo
"""
Exercise 5.4
Sqlite version of exercise:
We can select count of customerID on orders to get how many times each customer ordered a certain product and their ContactName
We join customers on orders, orders on order details and order details on products
We filter by ProductID which needs to be 7 and group by CustomerID to get distinct Customers
"""
con = sqlite3.connect("northwind.db")
con.text_factory = lambda x: str(x, 'latin1')
cur = con.cursor()
cur.execute("""SELECT Count(Orders.CustomerID), Customers.ContactName from Orders
			   INNER JOIN Customers on Orders.CustomerID = Customers.CustomerID 
			   INNER JOIN 'Order Details' on Orders.OrderID = 'Order Details'.OrderID 
			   INNER JOIN Products on 'Order Details'.ProductID = Products.ProductID  
			   WHERE Products.ProductID = 7 GROUP BY Orders.CustomerID""")
orders = cur.fetchall()
print("Sqlite: {} distinct people ordered Uncle Bob's Organic Dried Pears\n They are:".format(len(orders)))
for order in orders:
	print(order)
con.close()

""" MongoDB version of exercise:
In the MongoDB version we start with order details which contain the Pears Product ID
We iterate over their respective orders and the orders respective customers
We can then build a list of distinct customers which have ordered the Pears and also how many times they have ordered them
"""
client = pymongo.MongoClient('localhost', 27017)
db = client["Northwind"]
customer_collection = db["customers"]
order_collection = db["orders"]
order_details_collection = db["order-details"]
products_collection = db["products"]

customer_list = []
pear_details = order_details_collection.find({"ProductID":7})
for detail in pear_details:
	for order in order_collection.find({"OrderID": detail["OrderID"]}):
		for customer in customer_collection.find({"CustomerID":order["CustomerID"]}):
			customer_list.append(customer["ContactName"])

print("MongoDB: {} distinct people ordered Uncle Bobo's Organic Dried Pears\n They are:".format(len(set(customer_list))))
for customer in set(customer_list):
	print((customer_list.count(customer), customer))

