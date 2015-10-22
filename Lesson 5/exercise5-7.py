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

ALFKI_product_names = []
ALFKI_products = []

for ALFKI_order in order_collection.find({'CustomerID': 'ALFKI'}):
    for orderID in order_details_collection.find({'OrderID':ALFKI_order["OrderID"]}):
        if orderID['ProductID']:
            ALFKI_products.append(orderID['ProductID'])
        #for product in products_collection.find({'ProductID': orderID['ProductID']}):
            #if product['ProductName']:
            #    ALFKI_product_names.append(product['ProductName'])


ALFKI_product_names = set(ALFKI_product_names)
ALFKI_products = set(ALFKI_products)
print(ALFKI_products)
"""
for productID in order_details_collection.find({'ProductID': ALFKI_products})
    for orders in order_collection.find({'OrderID':productID['OrderID']}):
        if orders['CustomerID']
        pass
    for x in order_collection.find({'$and':[]
        pass
    pass
}

print(len(ALFKI_product_names))
print(ALFKI_product_names)
"""