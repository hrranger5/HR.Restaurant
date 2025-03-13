import mysql.connector

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",  # ya "localhost" try karo
        user="root",
        password="",  # Agar password nahi diya toh empty chhoro
        database="restaurant_chatbot"  # Apna actual database name likho
    )

    if connection.is_connected():
        print("✅ Database connection successful!")
except mysql.connector.Error as err:
    print("❌ Error:", err)
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
