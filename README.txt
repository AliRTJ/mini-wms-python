Mini Warehouse Management System (WMS) v.02
Overview

This project is a Python + MySQL mini Warehouse Management System designed to simulate basic warehouse operations.

The system allows users to manage products, track inventory, and process customer orders while validating available stock.

The goal of the project is to model real warehouse operational logic using programming and relational databases.

This project was built as a learning exercise while studying Python and SQL, combined with practical experience in supply chain and warehouse operations.

Features
Product Management

Add new products

View all products

Update product quantity

Delete products

Inventory Tracking

Inventory is stored in a MySQL database and updated automatically when orders are processed.

Inventory fields include:

on_hand

allocated

available

This simulates real warehouse inventory allocation logic.

Order Management

The system allows users to:

Create new orders

Validate product existence

Check inventory availability

Allocate inventory automatically

Generate backorders if stock is insufficient

Order Lifecycle

Orders move through different statuses:

ALLOCATED → Inventory available and reserved
BACKORDER → Insufficient inventory
SHIPPED → Order shipped and inventory consumed
CANCELLED → Order cancelled and inventory released

Shipping and Cancellation

Additional workflow functions include:

Ship allocated orders

Cancel orders

Automatically update inventory quantities

Reporting

## The system includes basic operational reports:

All orders report

Backorder report

Reports are generated using SQL JOIN queries between orders and products tables.

Tech Stack

Python
MySQL
MySQL Connector for Python

Database Structure
Products Table

## Stores product inventory information.

Fields:

id
pro_name
on_hand
allocated
available
price

Orders Table

## Stores customer order information.

Fields:

order_id
product_id
quantity
status

###Example Order Allocation Logic

Example scenario:

Inventory:

Product A = 100 units available

Customer order:

120 units

System behavior:

Inventory insufficient
Order status set to BACKORDER

If order quantity is less than available inventory:

Inventory is allocated
Order status becomes ALLOCATED

Running the Project

Install MySQL

Install MySQL Connector

pip install mysql-connector-python

Update database credentials in the code

host="localhost"
user="root"
password="root"
database="wms"

Run the Python program

python main.py

Menu Interface

The program runs through a command-line interface:

Add new product

Show all products

Update product quantity

Delete product

Create order

Process backorder

Ship order

Cancel order

Show all orders

Backorder report

Exit

Future Improvements

Possible enhancements:

Inventory transaction history
Product location management
Picking workflow
REST API version
Web interface
Dashboard reporting (Power BI / Python)

Purpose of the Project

This project demonstrates how warehouse operations can be modeled programmatically using Python and SQL.

It combines software development with real supply chain logic, similar to how enterprise Warehouse Management Systems operate.

Author

Alireza Taherijam

