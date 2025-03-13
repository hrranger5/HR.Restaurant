import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Google Cloud Service Account Key Path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Confirm if the path is correctly set
print("Service Account Key Path:", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

db_config = {
    "host": "localhost",     
    "user": "root",           
    "password": "",          
    "database": "restaurant_chatbot" 
}

try:
    connection = mysql.connector.connect(**db_config)
    print("✅ Database connection successful!")
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
