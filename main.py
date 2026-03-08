import mysql.connector

def get_connection(): # to connect to mysql database
    return mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= "root"
    )
def create_order_table(): # to crate order table in the beginning of the program
    conn = get_connection()
    mycursor = conn.cursor()
    sql_create_order_tabel = "" \
    "CREATE TABLE IF NOT EXISTS wms.orders " \
    "(order_id INT PRIMARY KEY AUTO_INCREMENT, " \
    "product_id INT, " \
    "quantity INT, " \
    "status VARCHAR(50))"
    mycursor.execute(sql_create_order_tabel)

def create_product_tabel(): #to create the product table
    conn = get_connection()
    mycursor = conn.cursor()
    sql_create_table = "" \
    "CREATE TABLE IF NOT EXISTS wms.products (id INT AUTO_INCREMENT PRIMARY KEY, " \
    "pro_name VARCHAR(50),  " \
    "quantity INT, " \
    "price DECIMAL(10,2)) "
    mycursor.execute(sql_create_table)
    
def add_product(): #to add product to inventory database
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
        "INSERT INTO wms.products (pro_name, quantity, price) " \
        "VALUES (%s, %s, %s)"
    mycursor.execute(sql_add_product, (pro_name, quantity, price))
    conn.commit()

def get_all_product(): # to fetch all product with inventory and show them
    conn = get_connection()
    mycursor = conn.cursor()
    fetch_all_product = "SELECT * FROM wms.products"
    mycursor.execute(fetch_all_product)
    result = mycursor.fetchall()
    for product in result:
        print("Product ID: ", product[0])
        print("Product name: ", product[1])
        print("Product Quantity: ", product[2])
        print("Product Price: ", product[3])
        print("------------------------------")



def update_product(): # to update product quantity after asking the product name and quantity to update
    conn = get_connection()
    mycursor = conn.cursor()
    id = int(input("Enter product ID to update quantity: "))
    update_qua = int(input("Enter quantity to update: "))
    update_pro = "UPDATE wms.products " \
                "SET quantity = %s " \
                "WHERE id = %s" # using %s to placeholder 
    mycursor.execute(update_pro, (update_qua, id))
    conn.commit()

def delete_product(): # to delete product from inventory
    conn = get_connection()
    mycursor = conn.cursor()
    try:
        id = int(input("Enter product ID to DELETE: "))
    except ValueError:
        print("ID is not valid")
        return
    delete_pro = "DELETE FROM wms.products WHERE id = %s"
    mycursor.execute(delete_pro, (id,))
    conn.commit()


def create_order(): # to create order 
    conn = get_connection()
    mycursor = conn.cursor()
    try:
        try:
            pro_id = int(input("Enter product ID: ")) # to get product ID from the user
            if pro_id not in product_id_verification(): # to verify product exists
                print("\nproduct ID is not exist\n")
                return
        except ValueError:
            print("product ID in not valid")
            return
        try:
            o_quantity = int(input("Enter order quantity: ")) # to get order quantity form the user
        except ValueError:
            print("quantity must be an intiger number.")
            return
        
        sql_check_inventory = "SELECT quantity FROM wms.products WHERE id = %s" # to validate porduct ID through product table
        mycursor.execute(sql_check_inventory, (pro_id,))
        result = mycursor.fetchone()
        if result is None:
            print("Product not found")
            conn.close()
            return
        
        inventory = result[0]
        if o_quantity <= inventory: # to check inventory and make decision logic 
            mycursor.execute("UPDATE wms.products SET quantity = quantity - %s WHERE id = %s", (o_quantity, pro_id))
            mycursor.execute("INSERT INTO wms.orders (product_id, quantity, status) VALUES (%s, %s, 'CONFIRMED')", (pro_id, o_quantity))
        else:
            mycursor.execute("INSERT INTO wms.orders (product_id, quantity, status) VALUES (%s, %s, 'BLOCKED')", (pro_id, o_quantity))
        conn.commit()
        mycursor.close()
        conn.close()
    
    except Exception as e:
        print(f"an error occurd: {e}")
        conn.rollback()    

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
    FROM wms.orders o 
    JOIN wms.products p  
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

def product_id_verification(): # to vrify the product id
    conn = get_connection()
    mycursor = conn.cursor()
    sql_ftch_prodcut_id = "SELECT id FROM wms.products"
    mycursor.execute(sql_ftch_prodcut_id)
    result = mycursor.fetchall()
    product_ids = [product[0] for product in result] # creating list of product id for verification
    #for product in result:
    #    product_ids.append(product[0])
    return product_ids

# main function menu to show the options
# create_order_table()
# create_product_tabel()
while True:
    try:
        print("1. Add new product")
        print("2. show all product")
        print("3. update product quntity")
        print("4. Delete product")
        print("5. Add new order")
        print("6. Show all orders")
        print("7. Exit")
        
        choice = int(input("Enter your choice: "))
        if choice == 1:        
            add_product()
        elif choice == 2:
            get_all_product()
        elif choice == 3:
            update_product()
        elif choice == 4:
            delete_product()
        elif choice == 5:
            create_order()
        elif choice == 6:
            show_all_orders()
        elif choice == 7:
            break
        else:
            print("Enter 1 or 6")
    except ValueError:
        print("\ninvalid choice\n")