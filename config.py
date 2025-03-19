import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",   
            user="root",       
            password="",       
            database="restaurant_chatbot"  
        )
        if connection.is_connected():
            print("Database connected successfully!")
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
