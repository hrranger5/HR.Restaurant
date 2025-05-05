from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import random
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import mysql.connector
from functools import wraps
import secrets
from datetime import datetime, timedelta
from flask_mail import Message
from flask_mail import Mail
from werkzeug.security import check_password_hash
from random import randint
from functools import wraps
import datetime 
import logging
import uuid
from dateutil.parser import parse as parse_datetime

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

CORS(app)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'baaa4647a590a6692560920062fa190dc9b402ac7d17989b0bc59f09eec45128'
app.config['SESSION_TYPE'] = 'filesystem'  
app.secret_key = os.urandom(24) 

jwt = JWTManager(app)


# MySQL Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="restaurant_chatbot"
    )
def generate_otp():
    return str(randint(100000, 999999))

# Set up the secret key and Flask-Mail configuration
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hrranger555@gmail.com'  
app.config['MAIL_PASSWORD'] = 'sgks iehx dicl uwol' 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/')
def home():
    # Pass user info to index template if logged in
    user_data = None
    if 'user_id' in session:
        user_data = {
            'id': session['user_id'],
            'username': session.get('username', ''),
            'role': session.get('role', '')
        }
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "customer")  # Default to customer, but allow admin selection
        
        # Input validation
        if not name or not email or not password:
            flash("All fields are required", "danger")
            return redirect(url_for('signup'))

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT email FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            flash("Email already registered", "warning")
            cursor.close()
            conn.close()
            return redirect(url_for('signup'))

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            # Insert new user
            cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                           (name, email, hashed_password, role))
            conn.commit()
            flash("Signup successful! Please log in.", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get user with role
        cursor.execute("""
            SELECT user_id, username, password_hash, role 
            FROM users WHERE email = %s
        """, (email,))
        user = cursor.fetchone()
        
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['user_role'] = user['role']  # ✅ This must match what the decorator checks

            
            # Redirect based on role
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
        
        cursor.close()
        conn.close()
        
    return render_template('login.html')


#------------------ Admin Dashboard ------------------#
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'admin':
            flash("Admin access required.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total Users
    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    users = cursor.fetchone()[0]  # Access the first element of the tuple

    # Total Orders
    cursor.execute("SELECT COUNT(*) AS total_orders FROM orders")
    orders = cursor.fetchone()[0]  # Access the first element of the tuple

    # Total Revenue (example)
    cursor.execute("SELECT SUM(total_amount) AS total_revenue FROM orders")
    revenue = cursor.fetchone()[0]  # Access the first element of the tuple

    # Pending Reservations
    cursor.execute("SELECT COUNT(*) AS pending_reservations FROM reservations WHERE status = 'Pending'")
    reservations = cursor.fetchone()[0]  # Access the first element of the tuple

    # Recent Orders (example)
    cursor.execute("SELECT order_id, created_at, total_amount FROM orders ORDER BY created_at DESC LIMIT 5")
    recent_orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_dashboard.html', 
                           total_users=users, 
                           total_orders=orders, 
                           revenue=revenue, 
                           pending_reservations=reservations, 
                           recent_orders=recent_orders)



#------------------ Admin Orders ------------------#
@app.route('/admin/orders')
@admin_required
def admin_orders():
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash("Admin access required.", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = cursor.fetchall()

    conn.close()
    return render_template('orders.html', orders=orders)

#------------------ Admin Reservations ------------------#
@app.route('/admin/reservations')
@admin_required
def admin_reservations():
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash("Admin access required.", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reservations ORDER BY reservation_date DESC")
    reservations = cursor.fetchall()

    conn.close()
    return render_template('reservations.html', reservations=reservations)

#------------------ Admin Feedback ------------------#
@app.route('/admin/feedback')
@admin_required
def admin_feedback():
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash("Admin access required.", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the query to use 'created_at' instead of 'submitted_at'
    cursor.execute("SELECT * FROM feedback ORDER BY created_at DESC")
    feedbacks = cursor.fetchall()

    conn.close()
    return render_template('feedback.html', feedbacks=feedbacks)

# Mock database (This will be replaced by real DB in production)
mock_db = {
    'admin': {
        'name': 'Hafsa',
        'email': 'hrranger555@gmail.com',
        'password': '$2b$12$hNLouuoztSjQeeu8/MbOWeVIk/ufxVjfZnLd2qirnnr...',  # Hashed password
        'profile_picture': 'default.jpg',  # Default profile picture
        'status': 'active',
        'role': 'admin',
        'created_at': '2025-04-27 18:44:25'
    }
}

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/setting', methods=['GET'])
def setting():
    # Get the admin data from mock DB
    admin = mock_db.get('admin')
    return render_template('setting.html', admin=admin)

@app.route('/admin/update-profile', methods=['POST'])
def update_profile():
    # Fetch the admin data from mock DB
    admin = mock_db.get('admin')

    # Get form input values
    name = request.form['name']
    email = request.form['email']
    password = request.form.get('password')  # Optional password change

    # Update admin data
    admin['name'] = name
    admin['email'] = email
    if password:
        admin['password'] = password  # Normally, hash the password before saving

    # Handle profile picture upload
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            admin['profile_picture'] = filename  # Update profile picture

    # Flash a success message
    flash("Profile updated successfully!", "success")

    # Redirect to settings page
    return redirect(url_for('setting'))

# User Dashboard Route
@app.route('/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    username = session['username']  # Assuming you stored the username in session when the user logged in

    # Fetch recent orders from the database
    conn = get_db_connection()  # Use the get_db_connection function here
    cursor = conn.cursor()
    cursor.execute("""
         SELECT order_id, created_at, total_amount, status 
         FROM orders 
         WHERE user_id = %s 
         ORDER BY created_at DESC 
         LIMIT 5
        """, (user_id,))
    order_data = cursor.fetchall()

    # Fetch upcoming reservations
    cursor.execute("""
    SELECT reservation_id, reservation_date, reservation_time, num_guests, status
    FROM reservations
    WHERE user_id = %s AND reservation_date >= %s
    ORDER BY reservation_date ASC
    LIMIT 5
    """, (user_id, datetime.date.today()))  # Use datetime.date.today() correctly
    reservation_data = cursor.fetchall()

    # Fetch cart items if applicable
    cart_items = session.get('cart_items', [])
    cart_total = sum(item['price'] * item['quantity'] for item in cart_items)  # Calculate the total

    # Process orders and reservations to add status color
    orders = []
    for row in order_data:
        orders.append({
            'id': row[0],
            'date': row[1],
            'items': row[2],
            'total': row[3],
            'status': row[4],
            'status_color': get_status_color(row[4])
        })

    reservations = []
    for row in reservation_data:
        reservations.append({
            'id': row[0],
            'date': row[1],
            'time': row[2],
            'guests': row[3],
            'status': row[4],
            'status_color': get_status_color(row[4])
        })

    return render_template('user_dashboard.html', username=username, orders=orders, reservations=reservations, cart_items=cart_items, cart_total=cart_total)

# Helper function to get status color for badges
def get_status_color(status):
    color_map = {
        'Delivered': 'success',
        'In Progress': 'warning',
        'Cancelled': 'danger',
        'Confirmed': 'info',
    }
    return color_map.get(status, 'secondary')


#-----forgot password route-------

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Verify user exists
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            # Generate and store OTP
            otp = generate_otp()
            expiry = datetime.now() + timedelta(minutes=10)
            
            cursor.execute("""
                INSERT INTO password_resets (user_id, otp, expires_at)
                VALUES (%s, %s, %s)
            """, (user['user_id'], otp, expiry))
            conn.commit()
            
            # Send OTP email
            if send_otp_email(email, otp):
                flash('OTP has been sent to your email.', 'success')
                return redirect(url_for('verify_otp', email=email))
            else:
                flash('Failed to send OTP. Please try again.', 'danger')
        else:
            flash('Email address not found.', 'danger')
        
        cursor.close()
        conn.close()
        
    return render_template('forgot_password.html')



# Assuming you have a function to get user details from the database
def get_user_from_db(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user



@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    otp = request.args.get('otp')  # Get OTP from URL
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Verify OTP
    cursor.execute("""
        SELECT user_id FROM otp_resets 
        WHERE otp = %s AND expires_at > NOW() AND used = 0
    """, (otp,))
    reset = cursor.fetchone()
    
    if not reset:
        flash('Invalid or expired OTP.', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
        else:
            # Update password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute("""
                UPDATE users SET password_hash = %s WHERE user_id = %s
            """, (hashed_password, reset['user_id']))
            
            # Mark OTP as used
            cursor.execute("""
                UPDATE otp_resets SET used = 1 WHERE otp = %s
            """, (otp,))
            
            conn.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('login'))
    
    cursor.close()
    conn.close()
    return render_template('reset_password.html', otp=otp)

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    email = request.args.get('email')
    
    if request.method == 'POST':
        otp = request.form.get('otp')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify OTP
        cursor.execute("""
            SELECT user_id FROM password_resets 
            WHERE otp = %s AND expires_at > NOW() AND used = 0
        """, (otp,))
        reset = cursor.fetchone()
        
        if reset:
            # Mark OTP as used
            cursor.execute("UPDATE password_resets SET used = 1 WHERE otp = %s", (otp,))
            conn.commit()
            
            # Generate password reset token
            token = secrets.token_urlsafe(32)
            return redirect(url_for('reset_password', token=token))
        else:
            flash('Invalid or expired OTP.', 'danger')
        
        cursor.close()
        conn.close()
        
    return render_template('verify_otp.html', email=email)


# Profile management
@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username, email, role FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for('login'))

# Menu routes
@app.route('/menu')
def menu():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items")
    menu_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('menu.html', menu_items=menu_items)

@app.route('/get_menu', methods=['GET'])
def get_menu():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items")
    menu = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(menu)

# Order routes
@app.route('/order')
def order():
    if 'user_id' not in session:
        flash("Please login to place an order", "warning")
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items")
    menu_items = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('order.html', menu_items=menu_items)

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        if request.is_json:
            return jsonify({"error": "Authentication required"}), 401
        else:
            flash("Please login to place an order", "warning")
            return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        # Get order items from form or JSON
        items = request.json.get('items') if request.is_json else request.form.getlist('items')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create order record
        cursor.execute("INSERT INTO orders (user_id, order_status) VALUES (%s, %s)", 
                      (user_id, 'pending'))
        conn.commit()
        order_id = cursor.lastrowid
        
        # Add order items
        for item in items:
            item_id = item.get('item_id') if request.is_json else item
            quantity = item.get('quantity', 1) if request.is_json else 1
            cursor.execute("INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)",
                          (order_id, item_id, quantity))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        if request.is_json:
            return jsonify({"message": "Order placed successfully!", "order_id": order_id}), 201
        else:
            flash("Order placed successfully!", "success")
            return redirect(url_for('myorders'))
            
    except Exception as e:
        if request.is_json:
            return jsonify({"error": str(e)}), 500
        else:
            flash(f"Error placing order: {str(e)}", "danger")
            return redirect(url_for('order'))


# Feedback routes
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        rating = request.form.get('rating')
        comments = request.form.get('comments')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO feedback (user_id, rating, comments)
                VALUES (%s, %s, %s)
            """, (user_id, rating, comments))
            
            conn.commit()
            flash("Thank you for your feedback!", "success")
            
        except Exception as e:
            flash(f"Error submitting feedback: {str(e)}", "danger")
            
        finally:
            cursor.close()
            conn.close()
            
        return redirect(url_for('feedback'))
        
    # GET request - show form
    return render_template('feedback.html')

# Order tracking
@app.route('/track_order', methods=['GET', 'POST'])
def track_order():
    if request.method == 'POST':
        order_id = request.form.get('order_id') or request.json.get('order_id')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE order_id=%s", (order_id,))
        order = cursor.fetchone()
        cursor.close()
        conn.close()

        if order:
            if request.is_json:
                return jsonify({"status": order['order_status']})
            else:
                return render_template('track_order.html', order=order)
        else:
            if request.is_json:
                return jsonify({"error": "Invalid Order ID"}), 404
            else:
                flash("Invalid Order ID", "danger")
                return render_template('track_order.html')
    
    # GET request - show form
    return render_template('track_order.html')

# API endpoints
@app.route('/api/order_status/<int:order_id>', methods=['GET'])
@jwt_required()
def order_status(order_id):
    current_user = get_jwt_identity()
    user_id = current_user.get('user_id')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Add user_id check for security
    cursor.execute("""
        SELECT order_status FROM orders 
        WHERE order_id=%s AND user_id=%s
    """, (order_id, user_id))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return jsonify({"order_status": result['order_status']})
    return jsonify({"message": "Order not found"}), 404

@app.route('/api/submit_feedback', methods=['POST'])
@jwt_required()
def api_submit_feedback():
    current_user = get_jwt_identity()
    user_id = current_user.get('user_id')
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO feedback (user_id, rating, comments)
            VALUES (%s, %s, %s)
        """, (user_id, data.get("rating"), data.get("comments")))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Feedback submitted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req['queryResult']['intent']['displayName']

    if intent == 'Make Reservation':
        return make_reservation(req)
    elif intent == 'Modify Reservation':
        return modify_reservation(req)
    elif intent == 'Order Tracking':  # Updated intent name
        return order_tracking(req)
    elif intent == 'AddToCart':
        return add_to_cart(req)
    elif intent == 'View Cart':
        return view_cart(req)
    elif intent == 'Place-Order':
        return place_order(req)
    elif intent == 'Modify Order':
        return modify_order(req)
    elif intent == 'Feedback':
        return submit_feedback(req)
    else:
        return jsonify({'fulfillmentText': "Sorry, I couldn't understand your request."})

def place_order(req):
    params = req.get("queryResult", {}).get("parameters", {})
    food_item = params.get("food_item")
    quantity = params.get("number", 1)
    user_id = params.get("user_id", 1)

    if not food_item:
        return jsonify({"fulfillmentText": "Please tell me what you'd like to order."})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Create order
        cursor.execute("INSERT INTO orders (user_id) VALUES (%s)", (user_id,))
        order_id = cursor.lastrowid

        # 2. Insert item
        cursor.execute(""" 
            INSERT INTO order_items (order_id, food_item, quantity) 
            VALUES (%s, %s, %s)
        """, (order_id, food_item, quantity))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "fulfillmentText": f"Order placed successfully! {quantity} x {food_item} added to Order #{order_id}."
        })

    except Exception as e:
        print("Order placement error:", e)
        return jsonify({"fulfillmentText": "Something went wrong while placing your order. Please try again."})

def make_reservation(req):
    from datetime import datetime
    import logging

    params = req.get("queryResult", {}).get("parameters", {})

    try:
        # 🔧 FIX: extract 'name' from nested dictionary
        name = params.get("person", {}).get("name", "Guest")
        phone = params.get("phone", "N/A")
        num_guests = params.get("num_guests", 1)

        date_str = params.get("date", "")
        time_str = params.get("time", "")

        # 🧠 Convert strings to datetime objects
        date_obj = parse_datetime(date_str)
        time_obj = parse_datetime(time_str)

        reservation_datetime = date_obj.replace(
            hour=time_obj.hour, minute=time_obj.minute
        )

        formatted_date = reservation_datetime.strftime("%Y-%m-%d")
        formatted_time = reservation_datetime.strftime("%I:%M %p")

        # ✅ Insert reservation into MySQL
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO reservations (person, phone, guests, date_time) VALUES (%s, %s, %s, %s)",
            (name, phone, num_guests, reservation_datetime)
        )

        conn.commit()

        response_text = (
            f"Thanks {name}, your table for {num_guests} guests is booked on "
            f"{formatted_date} at {formatted_time}. We'll contact you at {phone}."
        )

    except Exception as e:
        import traceback
        logging.error(f"Reservation error: {e}")
        logging.error(traceback.format_exc())
        response_text = "Something went wrong while saving your reservation."

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

    return jsonify({'fulfillmentText': response_text})
def order_tracking(req):
    parameters = req.get("queryResult", {}).get("parameters", {})
    order_id = parameters.get("order_id", None)

    if not order_id:
        return jsonify({
            "fulfillmentText": "Please provide a valid Order ID to track your order. For example, you can say 'My order ID is 12345'."
        })

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query the order_tracking table to fetch the status of the order
        cursor.execute("SELECT status FROM order_tracking WHERE order_id = %s", (order_id,))
        result = cursor.fetchone()

        if result:
            status = result['status']
            return jsonify({
                "fulfillmentText": f"🆔 Order ID: {order_id}\n📦 Status: {status}. \n🚚 Your order is being processed and will be dispatched soon."
            })
        else:
            return jsonify({
                "fulfillmentText": f"❌ No order found with Order ID: {order_id}. Please check and try again."
            })

    except Exception as e:
        print("Error tracking order:", e)
        return jsonify({
            "fulfillmentText": f"❌ Error while tracking your order: {str(e)}. Please try again later."
        })

    finally:
        cursor.close()
        conn.close()
def add_to_cart(req):
    parameters = req.get('queryResult', {}).get('parameters', {})
    items = parameters.get('food_items', [])
    quantities = parameters.get('number', [])

    # Ensure items is a list
    if isinstance(items, str):
        items = [items]
    elif not isinstance(items, list):
        items = list(items)

    # Ensure quantities is a list
    if isinstance(quantities, (int, float)):
        quantities = [quantities]
    elif not isinstance(quantities, list):
        quantities = list(quantities)

    # Safety check: length match
    if len(items) != len(quantities):
        return jsonify({'fulfillmentText': "Mismatch between items and quantities."})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create a new order without user_id if not used anymore
        cursor.execute("INSERT INTO orders () VALUES ()")
        conn.commit()
        new_order_id = cursor.lastrowid

        # Insert each item into the cart
        for item, quantity in zip(items, quantities):
            cursor.execute(
                "INSERT INTO cart (order_id, food_item, quantity) VALUES (%s, %s, %s)",
                (new_order_id, item, quantity)
            )

        conn.commit()
        response_text = f"{', '.join([f'{q} x {item}' for q, item in zip(quantities, items)])} added to your order (Order ID: {new_order_id})."

    except Exception as e:
        logging.error(f"Error adding items to cart: {str(e)}")
        response_text = f"Error adding items to cart: {e}"

    finally:
        cursor.close()
        conn.close()

    return jsonify({'fulfillmentText': response_text})
def submit_feedback(req):
    # Extract feedback details from the request
    parameters = req.get('queryResult', {}).get('parameters', {})
    feedback_text = parameters.get('feedback', '')
    user_id = parameters.get('user_id', '')

    # Validate that feedback and user_id are provided
    if not feedback_text:
        return jsonify({'fulfillmentText': "Please provide your feedback."})
    
    if not user_id:
        return jsonify({'fulfillmentText': "Please provide a valid user ID to submit feedback."})

    try:
        # Log the feedback details for debugging
        app.logger.info(f"Received feedback from user {user_id}: {feedback_text}")
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists before saving feedback
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        user_exists = cursor.fetchone()

        if not user_exists:
            return jsonify({'fulfillmentText': "User not found. Please register first."})

        # Insert feedback into the database
        cursor.execute(
            "INSERT INTO feedback (user_id, feedback_text) VALUES (%s, %s)",
            (user_id, feedback_text)
        )

        conn.commit()
        response_text = f"Thank you for your feedback! You said: {feedback_text}"

    except Exception as e:
        logging.error(f"Error submitting feedback: {str(e)}")
        response_text = f"Error submitting feedback: {e}"

    finally:
        cursor.close()
        conn.close()

    return jsonify({'fulfillmentText': response_text})


# Placeholder functions for the other intents
def modify_reservation(req): return jsonify({'fulfillmentText': 'Modify reservation functionality coming soon.'})
def track_order(req): return jsonify({'fulfillmentText': 'Track order functionality coming soon.'})
def view_cart(req): return jsonify({'fulfillmentText': 'View cart functionality coming soon.'})
def modify_order(req): return jsonify({'fulfillmentText': 'Modify order functionality coming soon.'})

if __name__ == '__main__':
    app.run(debug=True)
