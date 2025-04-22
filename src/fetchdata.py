import mysql.connector
from mysql.connector import Error

# Database connection config
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # replace with your MySQL password if set
            database='restaurant_chatbot'
        )
        if connection.is_connected():
            print("Connection established")
            return connection
    except Error as err:
        print(f"Error: {err}")
        return None

# Get order status by order_id
def get_order_status(order_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT order_status FROM orders WHERE order_id = %s", (order_id,))
        result = cursor.fetchone()
        return result
    except Error as err:
        print(f"Error fetching order status: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()

# Get reservation details for a user
def get_reservations(user_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reservations WHERE user_id = %s", (user_id,))
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error fetching reservations: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()

# Get feedback list
def get_feedback():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM feedback ORDER BY created_at DESC")
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error fetching feedback: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()
