from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
import random
from flask import session
from flask_bcrypt import Bcrypt
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash
from email.mime.text import MIMEText
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from db import get_db_connection
import mysql.connector


app = Flask(__name__)

CORS(app)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'baaa4647a590a6692560920062fa190dc9b402ac7d17989b0bc59f09eec45128'
app.config['SESSION_TYPE'] = 'filesystem'  
app.secret_key = os.urandom(24) 
jwt = JWTManager(app)



# MySQL Database Connection

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restaurant_chatbot"
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

# User Signup
from flask import flash  # Make sure this is imported

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "customer")

        if not username or not email or not password:
            flash("All fields are required", "danger")
            return redirect(url_for('signup'))

        cursor.execute("SELECT email FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            flash("Email already registered", "warning")  # ✅ Use flash here
            return redirect(url_for('signup'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                       (username, email, hashed_password, role))
        db.commit()
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    try:
        data = request.get_json() if request.is_json else request.form
        email = data.get("email")
        password = data.get("password")

        print("Received:", email, password)  # Debugging

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT user_id, username, password_hash FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        print("User from DB:", user)  # Debugging

        if not user or not bcrypt.check_password_hash(user[2], password):
            return jsonify({"error": "Invalid credentials"}), 401

        session['user_id'] = user[0]
        session['role'] = 'customer'

        access_token = create_access_token(identity={"user_id": user[0], "username": user[1]})

        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    
    except Exception as e:
        print("Login Error:", e)
        # More specific error message for debugging purposes
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# Dashboard Route (Only accessible if logged in)
@app.route('/dashboard')
def dashboard():
    try:
        user_id = session['user_id']
        
        # Database connection setup
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="restaurant_chatbot"  
        )
        cursor = conn.cursor()

        # Fetch user info from database
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        # Fetch orders
        cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
        orders = cursor.fetchall()

        # Fetch reservations
        cursor.execute("SELECT * FROM reservations WHERE user_id = %s", (user_id,))
        reservations = cursor.fetchall()

        # If admin, get all users and all orders
        all_users = all_orders = None
        if session.get('role') == 'admin':
            cursor.execute("SELECT * FROM users")
            all_users = cursor.fetchall()

            cursor.execute("SELECT * FROM orders")
            all_orders = cursor.fetchall()

        return render_template("dashboard.html",
                               user=user,
                               orders=orders,
                               reservations=reservations,
                               all_users=all_users,
                               all_orders=all_orders)

    except Exception as e:
        print("Error in /dashboard route:", e)
        return "Internal Server Error", 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

# Update Profile Route
@app.route('/update_profile', methods=['POST'])
def update_profile():
    user = User.query.get(session['user_id'])
    user.fullname = request.form['fullname']
    user.email = request.form['email']
    user.phone = request.form['phone']
    db.session.commit()

    return redirect(url_for('dashboard'))

# Update Password Route
@app.route('/update_password', methods=['POST'])
def update_password():
    user = User.query.get(session['user_id'])
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if old_password != user.password:
        return 'Old password is incorrect'

    if new_password != confirm_password:
        return 'New passwords do not match'

    user.password = new_password
    db.session.commit()

    return redirect(url_for('dashboard'))

# Logout Route
@app.route('/logout')

def logout():
    session.pop('user_id', None)
    session.pop('role', None)  # Clear the session role
    return redirect(url_for('login'))  # Redirect to login page

# Get Menu

@app.route('/get_menu', methods=['GET'])
def get_menu():
    cursor.execute("SELECT * FROM menu_items")
    menu = [{"item_id": row[0], "name": row[1], "description": row[2], "price": row[3]} for row in cursor.fetchall()]
    return jsonify(menu)

# Place Order (Secured)
@app.route('/place_order', methods=['POST'])
@jwt_required()
def place_order():
    try:
        current_user = get_jwt_identity()
        data = request.json
        items = data['items']

        cursor.execute("INSERT INTO orders (user_id, order_status) VALUES (%s, %s)", (current_user['user_id'], 'pending'))
        db.commit()
        order_id = cursor.lastrowid  

        for item in items:
            cursor.execute("INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)",
                           (order_id, item['item_id'], item['quantity']))
        
        db.commit()
        return jsonify({"message": "Order placed successfully!", "order_id": order_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#  Reservation System
@app.route('/make_reservation', methods=['POST'])
@jwt_required()
def make_reservation():
    current_user = get_jwt_identity()
    data = request.json

    cursor.execute("INSERT INTO reservations (user_id, num_guests, reservation_time) VALUES (%s, %s, %s)",
                   (current_user["user_id"], data["num_guests"], data["reservation_time"]))
    db.commit()

    return jsonify({"message": "Reservation added successfully!"})

@app.route('/track_order',methods=['GET', 'POST'])
def track_order():
    order_id = request.json.get('order_id')
    
    
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="restaurant_chatbot"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE order_id=%s", (order_id,))
    order = cursor.fetchone()
    print("DEBUG: Query Result ->", order)

    conn.close()

    if order:
        return jsonify({"status": order['order_status']})
    else:
        return jsonify({"error": "Invalid Order ID"}), 404
    
#  Order Status Check
@app.route('/order_status/<int:order_id>', methods=['GET'])
@jwt_required()
def order_status(order_id):
    cursor.execute("SELECT order_status FROM orders WHERE order_id=%s", (order_id,))
    result = cursor.fetchone()

    if result:
        return jsonify({"order_status": result[0]})
    return jsonify({"message": "Order not found"}), 404

# Submit Feedback
@app.route('/submit_feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    current_user = get_jwt_identity()
    data = request.json

    cursor.execute("INSERT INTO feedback (user_id, rating, comments) VALUES (%s, %s, %s)",
                   (current_user["user_id"], data["rating"], data["comments"]))
    db.commit()

    return jsonify({"message": "Feedback submitted successfully!"})


if __name__ == '__main__':
    app.run(debug=True) 