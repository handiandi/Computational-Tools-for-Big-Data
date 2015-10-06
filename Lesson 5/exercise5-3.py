#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import pymongo
"""
FIXTHIS: sqlite version
Exercise 5.3
Sqlite version of exercise:
"""
con = sqlite3.connect("northwind.db")
con.text_factory = lambda x: str(x, 'latin1')
cur = con.cursor()
cur.execute("SELECT Orders.CustomerID, Orders.OrderID, Products.ProductName from Orders INNER JOIN 'Order Details' on Orders.OrderID = 'Order Details'.OrderID INNER JOIN Products on 'Order Details'.ProductID = Products.ProductID  WHERE Orders.CustomerID = 'ALFKI'")
orders = cur.fetchall()
for order in orders:
	print(order)
con.close()

""" MongoDB version of exercise:
"""
client = pymongo.MongoClient('localhost', 27017)
db = client["Northwind"]
order_collection = db["orders"]
order_details_collection = db["order-details"]
products_collection = db["products"]

alfki_orders = order_collection.find({"CustomerID":"ALFKI"})
for order in alfki_orders:
	for detail in order_details_collection.find({"OrderID":order["OrderID"]}):
		if order_details_collection.find({"OrderID": detail["OrderID"]}).count() > 1:
			product = products_collection.find_one({"ProductID":detail["ProductID"]})
			print(order["CustomerID"], detail["OrderID"], product["ProductName"])