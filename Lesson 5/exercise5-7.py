#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import pymongo

"""
Exercise 5.7
Sqlite version of Exercise:
We have 3 SELECT clauses. Numbered from first/outer to last/most inner: (1), (2) and (3). 

(3) collects all ProductNames ordered by the customer 'ALFKI'
(2) collects all customers who have ordered any of the ProductNames from (1). This is GROUP BY CustomerID and ProductName
(1) selects distinct CustomerID from (2) and counts it. This is GROUP BY CustomerID, ORDER BY the count and select the first 5 records

"""
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

ALFKI_products = []

for ALFKI_order in order_collection.find({'CustomerID': 'ALFKI'}):
    ALFKI_products.extend(order_details_collection.find({'OrderID':ALFKI_order["OrderID"]}).distinct("ProductID"))

customer_product_dict = {}

for order in order_collection.find({"CustomerID":{"$ne":"ALFKI"}}):
    for order_detail in order_details_collection.find({
                                                        "$and":[
                                                             {"OrderID":order["OrderID"]},
                                                             {"ProductID":{"$in":ALFKI_products}} 
                                                             ]}):
            customer_product_dict.setdefault(order["CustomerID"],[]).append(order_detail["ProductID"])

most_bought_customers = sorted([(customer,len(set(products))) for (customer,products) in customer_product_dict.items()], key=lambda x: x[1], reverse=True)[:5]
for customer,count in most_bought_customers:
    print("{} products was bought by {}".format(count, customer))