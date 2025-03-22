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
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "customer")  # Default role is 'customer'

        if not username or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Check if email already exists
        cursor.execute("SELECT email FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already registered"}), 409

        # Hash the password before storing
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert user into the database
        cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                       (username, email, hashed_password, role))
        db.commit()

        return jsonify({"message": "User registered successfully!"}), 201

    return render_template('signup.html')  # Show signup form for GET requests

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Serve login page

    data = request.get_json() if request.is_json else request.form
    email, password = data.get("email"), data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    # Fetch user from database
    cursor.execute("SELECT user_id, username, password_hash FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user or not bcrypt.check_password_hash(user[2], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ Generate JWT Token
    access_token = create_access_token(identity={"user_id": user[0], "username": user[1]})

    return jsonify({"message": "Login successful", "access_token": access_token, "redirect": "/dashboard"}), 200

@app.route('/dashboard', methods=['GET'])
@jwt_required()  # ✅ Requires JWT token
def dashboard():
    try:
        current_user = get_jwt_identity()  # ✅ Get user info from JWT token

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ✅ Fetch user's orders
        cursor.execute("SELECT id, status FROM orders WHERE user_id = %s", (current_user["user_id"],))
        orders = cursor.fetchall()

        # ✅ Fetch user's reservations
        cursor.execute("SELECT id, date FROM reservations WHERE user_id = %s", (current_user["user_id"],))
        reservations = cursor.fetchall()

        conn.close()

        return jsonify({
            "message": f"Welcome, {current_user['username']}!",
            "orders": orders,
            "reservations": reservations
        }), 200

    except Exception as e:
        print(f"DEBUG: Dashboard Error - {str(e)}")
        return jsonify({"error": "Something went wrong. Please try again later."}), 500

@app.route('/customer_dashboard')
def customer_dashboard():
    return render_template('dashboard.html')

#  Forgot Password Route

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')  # Serve the HTML form

    data = request.get_json() if request.is_json else request.form
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required!"}), 400

    otp = str(random.randint(100000, 999999))  # Generate OTP
    session['reset_otp'] = otp
    session['reset_email'] = email  # Store email in session for later verification

    if send_email(email, otp):
        return jsonify({"message": "OTP sent successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send OTP!"}), 500


# Verify OTP
@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.json
    entered_otp = data.get("otp")

    if entered_otp == str(session.get("reset_otp")):
        session['otp_verified'] = True
        return jsonify({"message": "OTP verified!", "redirect": "/reset_password"}), 200
    else:
        return jsonify({"error": "Invalid OTP."}), 400

    

@app.route('/reset_password', methods=['GET'])
def reset_password():
    if 'otp_verified' not in session or not session['otp_verified']:
        return redirect(url_for('login'))  # Redirect to login if OTP is not verified

    return render_template('reset_password.html')  # Serve reset password form


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email, otp):
    sender_email = "hrranger555@gmail.com"
    sender_password = "zhtl xmxg rqyb tuvg"  # Use your new App Password

    subject = "Your OTP for Password Reset"
    body = f"Your OTP for password reset is: {otp}\n\nIf you did not request this, please ignore."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Create SMTP session for sending the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)  # Enable debugging
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Login using App Password
        server.sendmail(sender_email, to_email, msg.as_string())  # Send email
        server.quit()

        print(f"✅ OTP sent successfully to {to_email}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication Error: Check your App Password or enable Less Secure Apps.")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error: {str(e)}")
        return False

# Reset Password Using OTP (Step 1: Verify OTP)
@app.route('/reset_password_step1', methods=['POST'])
def reset_password_step1():
    if 'otp_verified' not in session or not session['otp_verified']:
        return jsonify({"error": "Unauthorized request"}), 401

    data = request.json
    entered_otp = data.get("otp")  # OTP from user

    if entered_otp != str(session.get('reset_otp')):
        return jsonify({"error": "Invalid OTP"}), 400

    session['otp_verified'] = True  # Mark OTP as verified
    return jsonify({"message": "OTP verified successfully!"}), 200

# Reset Password (Step 2: Set New Password)
@app.route('/reset_password_step2', methods=['POST'])
def reset_password_step2():
    if 'otp_verified' not in session or not session['otp_verified']:
        return jsonify({"error": "Unauthorized request"}), 401

    data = request.json
    new_password = data.get("new_password")

    if not new_password:
        return jsonify({"error": "Password is required"}), 400

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    
    cursor.execute("UPDATE users SET password_hash=%s WHERE email=%s", 
                   (hashed_password, session['reset_email']))
    db.commit()

    session.clear()  # ✅ Clear session after password reset
    return jsonify({"message": "Password reset successfully!", "redirect": "/login"}), 200


#  Profile Update
@app.route('/update_profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    data = request.json

    new_name = data.get("username")
    new_email = data.get("email")

    cursor.execute("UPDATE users SET username=%s, email=%s WHERE user_id=%s", 
                   (new_name, new_email, current_user["user_id"]))
    db.commit()

    return jsonify({"message": "Profile updated successfully!"})

@app.route('/add_menu_item', methods=['POST'])
def add_menu_item():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    image_url = data.get('image_url')

    if not name or not price or not image_url:
        return jsonify({"error": "Missing required fields"}), 400

    sql = "INSERT INTO menu_items (name, price, image_url) VALUES (%s, %s, %s)"
    values = (name, price, image_url)
    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Menu item added successfully"}), 201

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
