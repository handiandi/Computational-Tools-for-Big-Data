#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import pymongo
""" Sqlite version of exercise:
 First we need to join 3 tables which are of importance to us: Orders which contain single orders for a Customer,
  Order Details which ties an Order together with a Product and also contains quantity, price and discount,
  lastly we need the Products table to get the Product Name.
  So we join Orders and Order Details on OrderID, and Order Details and Products on ProductID, and then we only need the orders with ALFKI as customer.
  We then specify the attributes which are interesting, for example CustomerID to ensure ALFKI is Customer, the OrderID and the different Product Names in the order.
"""
print("sqlite part:")
try:
	con = sqlite3.connect("northwind.db")
	con.text_factory = lambda x: str(x, 'latin1')
	cur = con.cursor()
	cur.execute("""SELECT Orders.CustomerID as cID, Orders.OrderID as orID, Products.ProductName as pName from Orders 
					INNER JOIN 'Order Details' on orID = 'Order Details'.OrderID 
					INNER JOIN Products on 'Order Details'.ProductID = Products.ProductID  
					WHERE cID = 'ALFKI'""")
	orders = cur.fetchall()
	for order in orders:
		print(order)

except sqlite3.Error as e:
	print("Error {}".format(e.args[0]))
finally:
	if con:
		con.close()
""" MongoDB version of exercise:
The MongoDB version is sort of the same as the sqlite one, instead of joins we just iterate over queries of each collection with our chosen criteria 
"""
print("\nMongoDB part:")
client = pymongo.MongoClient('localhost', 27017)
db = client["Northwind"]
order_collection = db["orders"]
order_details_collection = db["order-details"]
products_collection = db["products"]

alfki_orders = order_collection.find({"CustomerID":"ALFKI"})
for order in alfki_orders:
	for detail in order_details_collection.find({"OrderID":order["OrderID"]}):
		product = products_collection.find_one({"ProductID":detail["ProductID"]})
		print(order["CustomerID"], detail["OrderID"], product["ProductName"])
