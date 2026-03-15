from products import *
from orders import *
from report import *
from logger_config import setup_logger
import logging

setup_logger() #initializing logger

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
        print("7. backorder")
        print("8. Ship order")
        print("9. cancel order")
        print("10. Backorder report")
        print("11. EXIT")
        
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
            create_backorder()
        elif choice == 8:
            ship_order()
        elif choice == 9:
            cancel_order()
        elif choice == 10:
            backorder_report()
        elif choice == 11:
            break
        else:
            print("Enter 1 or 11")
    except ValueError:
        print("\ninvalid choice\n")