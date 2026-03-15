import mysql.connector

def get_connection(): # to connect to mysql database
    return mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= "root",
        database="wms"
    )