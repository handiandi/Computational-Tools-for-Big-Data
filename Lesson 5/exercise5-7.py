#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import pymongo

con = sqlite3.connect("northwind.db")
con.text_factory = lambda x: str(x, 'latin1')
cur = con.cursor()
cur.execute("""SELECT DISTINCT outerSelect.cID, count(outerSelect.cID) as no_cID FROM  
                (SELECT Orders.CustomerID as cID from Orders
                    INNER JOIN 'Order Details' on Orders.OrderID = 'Order Details'.OrderID 
                    INNER JOIN Products on 'Order Details'.ProductID = Products.ProductID  
                    WHERE Products.ProductName in 
                        (SELECT DISTINCT Products.ProductName as pName FROM Orders 
                        INNER JOIN 'Order Details' on Orders.OrderID = 'Order Details'.OrderID 
                        INNER JOIN Products on 'Order Details'.ProductID = Products.ProductID  
                        WHERE Orders.CustomerID  = 'ALFKI')
                    GROUP BY cID, Products.ProductName) outerSelect
                WHERE outerSelect.cID != "ALFKI"
                GROUP BY outerSelect.cID ORDER BY no_cID DESC LIMIT 5""")

customers = cur.fetchall() 

con.close()
print("Sqlite part:\n----------------")
for cust, freq in customers:
    print("{} products was bought by {}".format(freq, cust))



print("\nMongoDB part:\n---------------")
client = pymongo.MongoClient('localhost', 27017)
db = client["Northwind"]
customer_collection = db["customers"]
order_collection = db["orders"]
order_details_collection = db["order-details"]
products_collection = db["products"]

ALFKI_product_names = []

for ALFKI_order in order_collection.find({'CustomerID': 'ALFKI'}):
    for orderID in order_details_collection.find({'OrderID':ALFKI_order["OrderID"]}):
        for product in products_collection.find({'ProductID': orderID['ProductID']}):
            if product['ProductName']:
                ALFKI_product_names.append(product['ProductName'])


ALFKI_product_names = set(ALFKI_product_names)
print(len(ALFKI_product_names))
print(ALFKI_product_names)