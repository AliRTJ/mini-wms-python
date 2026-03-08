# Mini Warehouse Management System (WMS)

## Overview

This project is a **Python + MySQL mini Warehouse Management System** designed to simulate basic warehouse operations.

The system allows users to manage products, track inventory, and create customer orders while validating available stock.

The goal of the project is to model **real warehouse operational logic** using programming and databases.

This project was built as a learning exercise while studying **Python and SQL**, combined with practical experience in **supply chain and warehouse operations**.

---

## Features

### Product Management

* Add new products
* View all products
* Update product quantity
* Delete products

### Inventory Tracking

* Inventory stored in MySQL database
* Automatic quantity updates when orders are confirmed

### Order Management

* Create new orders
* Validate product existence
* Check inventory availability
* Confirm order if inventory is sufficient
* Block order if inventory is insufficient

### Order Status Logic

Orders can have different statuses:

* `CONFIRMED` → Inventory available, order accepted
* `BLOCKED` → Not enough inventory

Future improvement:

* Partial allocation
* Backorder logic

---

## Tech Stack

* **Python**
* **MySQL**
* **MySQL Connector for Python**

---

## Database Structure

### Products Table

Stores product inventory information.

Fields:

* `id`
* `pro_name`
* `quantity`
* `price`

### Orders Table

Stores customer order information.

Fields:

* `order_id`
* `product_id`
* `quantity`
* `status`

---

## Example Order Logic

Example scenario:

Inventory:
Product A = 100 units

Customer order:
120 units

System behavior:

* Inventory insufficient
* Order status set to **BLOCKED**

If order quantity is less than available inventory:

* Inventory is reduced
* Order status becomes **CONFIRMED**

---

## Running the Project

1. Install MySQL
2. Install MySQL Connector

```bash
pip install mysql-connector-python
```

3. Update database credentials in the code

```python
host="localhost"
user="root"
password="root"
```

4. Run the Python program

```bash
python main.py
```

---

## Menu Interface

The program runs through a command-line interface:

1. Add new product
2. Show all products
3. Update product quantity
4. Delete product
5. Add new order
6. Show all orders
7. Exit

---

## Future Improvements

Planned enhancements:

* Order allocation logic
* Backorder management
* Inventory transaction history
* Location management
* Picking and shipping workflow
* Basic reporting

---

## Purpose of the Project

This project was built to combine **programming with real warehouse operations**.

It demonstrates how inventory and order processing logic can be modeled using **Python and SQL**, similar to how real warehouse management systems operate.

---

## Author

Alireza Taherijam
