from db import get_connection
import logging

def backorder_report():
    logging.info("Starting backorder_report")
    conn = get_connection()
    mycursor = conn.cursor()
    mycursor.execute("""
                   SELECT order_id, product_id, products.pro_name, quantity, status  
                    FROM orders
                    JOIN products
	                    ON orders.product_id = products.id
                    WHERE status = 'BACKORDER';
                     """)
    result =  mycursor.fetchall()
    for backorder in result:
        if not result:
            print("NO backorder found.")
        else:
            print(f"Order {backorder[0]} product {backorder[2]} quantity {backorder[3]}")
    mycursor.close()
    conn.close()
    logging.info("Backorder_report completed")



