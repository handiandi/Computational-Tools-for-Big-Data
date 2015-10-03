#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import pymongo

# first we try connecting and querying the sqlite database
# we can try to query all customers as well as orders for a specific customer
print("sqlite query:")
try:
	con = sqlite3.connect("northwind.db")
	con.text_factory = lambda x: str(x, 'latin1')
	cur = con.cursor()
	cur.execute("SELECT * from Customers LIMIT 1")
	first_customer = cur.fetchall()
	print(first_customer)
	cur.execute("SELECT * from Orders where Orders.CustomerID = 'ALFKI' ")
	order = cur.fetchone()
	print(order)

except sqlite3.Error as e:
	print("Error {}".format(e.args[0]))
finally:
	if con:
		con.close()
print("\n\n")

# next we try the same thing on the mongodb
print("mongodb query:")
client = pymongo.MongoClient('localhost', 27017)
db = client["Northwind"]
customer_collection = db["customers"]
first_customer = customer_collection.find_one()
print(first_customer)
order_collection = db["orders"]
order = order_collection.find_one({"CustomerID":"ALFKI"})
print(order)