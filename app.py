from flask import Flask, send_from_directory, request, jsonify
import mysql.connector
from functools import wraps
from dotenv import load_dotenv
import os
from google.cloud import dialogflow_v2 as dialogflow
import jwt
import datetime
import re
from werkzeug.security import generate_password_hash, check_password_hash

# Load Environment Variables
load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set!")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

# Flask App Initialization
app = Flask(__name__, static_folder='assets', template_folder='templates')
SECRET_KEY = "my_secret_key"

# Serve Static Files
@app.route('/assets/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Token Functions
def generate_token(user_id):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode({"user_id": user_id, "exp": exp_time}, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired!"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token!"}

# Authentication Decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        decoded = verify_token(token.split(" ")[1])
        if "error" in decoded:
            return jsonify(decoded), 401
        return f(*args, **kwargs)
    return decorated

# Database Connection Function
def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB", "restaurant_chatbot")
        )
    except mysql.connector.Error as e:
        print(f"🚨 Database connection failed: {e}")
        return None

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name, email, password = data.get('name'), data.get('email'), data.get('password')
    if not all([name, email, password]):
        return jsonify({"error": "All fields are required"}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid email format"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    hashed_password = generate_password_hash(password)

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        conn.commit()
        return jsonify({"success": True, "message": "User registered successfully!"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists!"}), 400
    finally:
        conn.close()

# Place Order Route
@app.route('/orders', methods=['POST'])
@requires_auth
def place_order():
    data = request.get_json()
    token = request.headers.get("Authorization").split(" ")[1]
    decoded = verify_token(token)
    user_id = decoded.get("user_id")

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (user_id, order_details, order_status) VALUES (%s, %s, %s)", (user_id, data.get("order_details"), "pending"))
        conn.commit()
        return jsonify({"success": True, "message": "Order placed successfully!"}), 201
    finally:
        conn.close()

# Get Orders Route
@app.route('/orders', methods=['GET'])
@requires_auth
def get_orders():
    token = request.headers.get("Authorization").split(" ")[1]
    decoded = verify_token(token)
    user_id = decoded.get("user_id")

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
        return jsonify(cursor.fetchall())
    finally:
        conn.close()

# Update Order Status Route
@app.route('/orders/<int:order_id>/status', methods=['PUT'])
@requires_auth
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get("order_status")

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET order_status = %s WHERE id = %s", (new_status, order_id))
        conn.commit()
        return jsonify({"success": True, "message": "Order status updated!"})
    finally:
        conn.close()

# Run Flask Server
if __name__ == '__main__':
    print("🔹 Starting Flask API...")
    app.run(host='0.0.0.0', port=5001, debug=True)
