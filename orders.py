from db import get_connection
import logging
def create_order_table(): # to create order table in the beginning of the program
    conn = get_connection()
    mycursor = conn.cursor()
    sql_create_order_tabel = "" \
    "CREATE TABLE IF NOT EXISTS orders " \
    "(order_id INT PRIMARY KEY AUTO_INCREMENT, " \
    "product_id INT, " \
    "quantity INT, " \
    "status VARCHAR(50))"
    mycursor.execute(sql_create_order_tabel)
    mycursor.close()
    conn.close()


def create_order(): # to create order 
    logging.info("strating create_order()")
    conn = get_connection()
    mycursor = conn.cursor()
    try:
        try:
            pro_id = int(input("Enter product ID: ")) # to get product ID from the user
        #    if pro_id not in product_id_verification(): # to verify product exists
        #        print("\nproduct ID is not exist\n")
            
        except ValueError:
            print("product ID in not valid")
            return
        try:
            o_quantity = int(input("Enter order quantity: ")) # to get order quantity form the user
        except ValueError:
            print("quantity must be an intiger number.")
            return
        
        # to validate product ID through product table and inventory check
        mycursor.execute("""SELECT available 
                         FROM products 
                         WHERE id = %s""", 
                         (pro_id,))
        
        result = mycursor.fetchone()
        if result is None:
            print("Product not found\n")
            conn.close()
            return
        
        inventory = result[0]
        if o_quantity <= inventory: # to check inventory and make decision logic 
            mycursor.execute("""UPDATE products 
                            SET allocated = allocated + %s,
                            available = on_hand - allocated
                            WHERE id = %s""", 
                            (o_quantity, pro_id))
            
            mycursor.execute("""INSERT INTO orders 
                             (product_id, quantity, status) 
                             VALUES (%s, %s, 'ALLOCATED')""", 
                             (pro_id, o_quantity))
            logging.info(f"order created: product {pro_id},| quantity: {o_quantity}")
        else:
            mycursor.execute("INSERT INTO orders (product_id, quantity, status) VALUES (%s, %s, 'BACKORDER')", (pro_id, o_quantity))
            logging.info(f" backorder created: product: {pro_id} | quantity: {o_quantity}")
        conn.commit()
        mycursor.close()
        conn.close()
        logging.info("create order completed")
        
    
    except Exception as e:
        print(f"an error occurred: {e}")
        conn.rollback() 
        logging.info("Error in create_error")   
    
def create_backorder(): # to process backorder, change order status, update available and allocated column from products table
    logging.info("starting create_backorder()")
    conn = get_connection()
    mycursor = conn.cursor()
    
    try:
        order_id = int(input("Enter order ID to backorder processing: "))
    except ValueError:
        print("Invalid order ID")
        return
    mycursor.execute("""SELECT product_id, quantity, available
                    FROM orders
                    INNER JOIN products
                        ON orders.product_id = products.id
                    WHERE order_id = %s AND status = 'BACKORDER'
                     """, (order_id,))
    result = mycursor.fetchone()
    if result is None:
        print("Backorder not found")
        conn.close()
        return
    product_id = result[0]
    backorder_qty = result[1]
    available = result[2]
    if backorder_qty <= available:
        mycursor.execute("""UPDATE orders SET status = 'ALLOCATED'
                         WHERE order_id = %s
                         """, (order_id,))
        mycursor.execute("""UPDATE products 
                         SET allocated = allocated + %s,
                         available = available - %s
                         WHERE id = %s
                         """,(backorder_qty, backorder_qty, product_id))
        logging.info(f"backorder processed: order {order_id} allocated")
    else:
        print("not sufficient stock")
        logging.info(f"backorder processed: order {order_id} insufficient stock")
    conn.commit()
    conn.close()
    logging.info("create_backorder completed")
    mycursor.close()
    conn.close()

def ship_order():
    logging.info("Starting ship_order")
    conn = get_connection()
    mycursor = conn.cursor()
    try:
        ship_o = int(input("Enter order number to ship: "))
    except ValueError:
        print("invalid order number.")
        return
    mycursor.execute("""SELECT product_id, quantity 
                     FROM orders
                     WHERE order_id = %s;                     
                     """, (ship_o,))
    result = mycursor.fetchone()

    if result is None:
        print("order not found")
        conn.close()
        return
    
    product_id = result[0]
    order_qty = result[1]
    mycursor.execute("""
                    UPDATE orders SET status = "SHIPPED" 
                     WHERE order_id = %s
                     """, (ship_o,))
    mycursor.execute("""
                    UPDATE products 
                    SET on_hand = on_hand - %s,
                    allocated = allocated - %s,
                    available = on_hand - allocated
                     WHERE id = %s
                     """, (order_qty, order_qty, product_id))
    mycursor.close()
    conn.commit()
    conn.close()
    logging.info(f"ship order: order {ship_o} was shipped")
    logging.info("ship_order completed")

def cancel_order():
    logging.info("Starting Cancel_order")
    conn = get_connection()
    mycursor = conn.cursor()
    try:
        cancel_o = int(input("Enter order number to cancel: "))
    except ValueError:
        print("Order number is not valid")
        return
    mycursor.execute("""
                    SELECT product_id, quantity
                    FROM orders
                    WHERE order_id = %s;                    
                     """, (cancel_o, cancel_o))
    result = mycursor.fetchone()

    if result is None:
        print("order not found")
        conn.close()
        return
    
    product_id = result[0]
    order_qty = result[1]
    mycursor.execute("""UPDATE orders SET status = 'CANCELLED'
                    WHERE order_id = %s;
                     """, (cancel_o, ))
    mycursor.execute("""
                    UPDATE products 
                    SET on_hand = on_hand + %s,
                        allocated = allocated - %s,
                        available = available + %s
                     WHERE id = %s
                     """, (order_qty, order_qty, order_qty, product_id))
    mycursor.close()
    conn.commit()
    conn.close()
    logging.info(f"Cancel order: order {cancel_o} was cancelled")
    logging.info("order_cancel completed")

def show_all_orders():
    conn = get_connection()
    mycursor = conn.cursor()
    mycursor.execute(""" 
    SELECT o.order_id, 
            o.product_id, 
            p.pro_name, 
            o.quantity AS order_quantity, 
            p.price, 
            o.status 
    FROM orders o 
    JOIN products p  
    ON o.product_id = p.id
    """)

    result = mycursor.fetchall()
    
    for order in result:
        print(f"order ID: {order[0]}")
        print(f"Product ID: {order[1]}")
        print(f"product name: {order[2]}")
        print(f"order quantity: {order[3]}")
        print(f"order price: {order[4]}")
        print(f"order status: {order[5]}")
        print("-------------------------")
    mycursor.close()
    conn.close()
