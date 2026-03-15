from db import get_connection
from logger_config import setup_logger
import logging

def create_product_table(): #to create the product table
    conn = get_connection()
    mycursor = conn.cursor()
    sql_create_table = """CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY, 
    pro_name VARCHAR(50), 
    on_hand INT, 
    allocated INT, 
    available INT, 
    price DECIMAL(10,2)) """
    mycursor.execute(sql_create_table)
    mycursor.close()
    conn.close()
    
def add_product(): #to add product to inventory database
    logging.info("starting add_product()")
    conn = get_connection()
    mycursor = conn.cursor()
    pro_name = input("Enter product name: ").strip()
    try:
        quantity = int(input("Enter product quantity: "))
    except:
        print("Quntity Must be anumber")
        return
    price = float(input("Enter product price: "))

    # insert the order into the order table
    sql_add_product = "" \
        "INSERT INTO products (pro_name, on_hand, allocated, available, price) " \
        "VALUES (%s, %s,'0',%s, %s)"
    mycursor.execute(sql_add_product, (pro_name, quantity,quantity, price))
    conn.commit()
    logging.info(f"Product added: {pro_name}, quantity: {quantity}")
    logging.info("add_produt completed")
    mycursor.close()
    conn.close()
    

def get_all_product(): # to fetch all product with inventory and show them
    conn = get_connection()
    mycursor = conn.cursor()
    fetch_all_product = "SELECT * FROM products"
    mycursor.execute(fetch_all_product)
    result = mycursor.fetchall()
    for product in result:
        print("Product ID: ", product[0])
        print("Product name: ", product[1])
        print("Product on hand Quantity: ", product[2])
        print("Product Price: ", product[3])
        print("------------------------------")
    mycursor.close()
    conn.close()

def update_product(): # to update product quantity after asking the product name and quantity to update
    logging.info("strting update_product()")
    conn = get_connection()
    mycursor = conn.cursor()
    id = int(input("Enter product ID to update quantity: "))
    update_qty = int(input("Enter quantity to update: "))
    update_pro = """UPDATE products 
                SET on_hand = on_hand + %s,
                available = (on_hand + %s) - allocated
                WHERE id = %s""" # using %s to placeholder 
    mycursor.execute(update_pro, (update_qty,update_qty, id))
    conn.commit()
    logging.info(f"product ID: {id} | quantity updated {update_qty}")
    logging.info("Update_product completed")
    mycursor.close()
    conn.close()

def delete_product(): # to delete product from inventory
    logging.info("Starting Delete_product()")
    conn = get_connection()
    mycursor = conn.cursor()
    try:
        id = int(input("Enter product ID to DELETE: "))
    except ValueError:
        print("ID is not valid")
        return
    delete_pro = "DELETE FROM products WHERE id = %s"
    mycursor.execute(delete_pro, (id,))
    conn.commit()    
    logging.info(f"Product ID: {id} was deleted")
    logging.info("delete_product completed")
    mycursor.close()
    conn.close()

def product_id_verification(): # to vrify the product id
    conn = get_connection()
    mycursor = conn.cursor()
    sql_ftch_prodcut_id = "SELECT id FROM products"
    mycursor.execute(sql_ftch_prodcut_id)
    result = mycursor.fetchall()
    product_ids = [product[0] for product in result] # creating list of product id for verification
    #for product in result:
    #    product_ids.append(product[0])
    conn.close()
    mycursor.close()
    conn.close()
    return product_ids
    
    