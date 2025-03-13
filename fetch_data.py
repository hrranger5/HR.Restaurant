import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),  # Use environment variable for password
        database="restaurant_chatbot"  # Ensure this database exists
    )

# Fetch customers function
def fetch_customers():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM customers")  # Ensure the 'customers' table exists
                customers = cursor.fetchall()

        if customers:
            for customer in customers:
                print(customer)  # Print fetched customers for debugging
        else:
            print("No customers found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Fetch menu items function
def fetch_menu_items():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM menu")  # Ensure the 'menu' table exists
                menu_items = cursor.fetchall()

        if menu_items:
            for item in menu_items:
                print(item)  # Print fetched menu items for debugging
        else:
            print("No menu items found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    fetch_customers()  # Call fetch function to test
    fetch_menu_items()  # Call fetch menu items function to test
