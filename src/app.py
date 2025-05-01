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

app = Flask(__name__)

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
@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Process payment logic goes here
    card_number = request.form['card_number']
    # Further processing such as payment gateway integration

    return redirect(url_for('user_dashboard'))  # Redirect to the dashboard or any other page after processing

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
            
@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    if 'user_id' not in session:
        if request.is_json:
            return jsonify({"error": "Authentication required"}), 401
        else:
            flash("Please login to make a reservation", "warning")
            return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        # Getting data from the request
        data = request.get_json() if request.is_json else request.form
        guest_count = data.get('guest_count')
        reservation_time = data.get('reservation_time')

        # Validate inputs
        if not guest_count or not reservation_time:
            if request.is_json:
                return jsonify({"error": "Missing required fields"}), 400
            else:
                flash("All fields are required", "danger")
                return redirect(url_for('reservations'))

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert reservation into the database
        cursor.execute("""
            INSERT INTO reservations (user_id, guest_count, reservation_time, status) 
            VALUES (%s, %s, %s, %s)
        """, (user_id, guest_count, reservation_time, 'pending'))
        
        conn.commit()
        cursor.close()
        conn.close()

        if request.is_json:
            return jsonify({"message": "Reservation made successfully"}), 200
        else:
            flash("Reservation made successfully", "success")
            return redirect(url_for('reservations'))
            
    except Exception as e:
        if request.is_json:
            return jsonify({"error": str(e)}), 500
        else:
            flash(f"Error making reservation: {str(e)}", "danger")
            return redirect(url_for('reservations'))

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
    intent = req.get('queryResult').get('intent').get('displayName')
    parameters = req.get('queryResult').get('parameters')
    
    response_text = "Sorry, I couldn't process your request."

    if intent == 'order_tracking':
        response_text = "Your order is on the way and will arrive in 20 minutes."

    elif intent == 'Cancel_Reservation':
        response_text = "Your reservation has been successfully canceled."

    elif intent == 'AddToCart':
        food_item = parameters.get('food_item')
        quantity = parameters.get('number', 1)
        user_id = parameters.get('user_id', 1)

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="restaurant_chatbot"
            )
            cursor = conn.cursor()

            insert_query = "INSERT INTO cart (user_id, food_item, quantity) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (user_id, food_item, quantity))
            conn.commit()

            response_text = f"{quantity} {food_item}(s) added to your cart. Your user ID is {user_id}. Please save this ID to view your cart later."

        except Exception as e:
            print("Database Error:", e)
            response_text = "There was an error adding the item to your cart."

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    elif intent == 'ViewCart':
        user_id = parameters.get('user_id', 1)

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="restaurant_chatbot"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT food_item, quantity FROM cart WHERE user_id = %s", (user_id,))
            rows = cursor.fetchall()

            if rows:
                cart_items = "\n".join([f"{qty} x {item}" for item, qty in rows])
                response_text = f"Your cart contains:\n{cart_items}"
            else:
                response_text = "Your cart is currently empty."

        except Exception as e:
            print("ViewCart Error:", e)
            response_text = "Unable to fetch your cart items."

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return jsonify({
        "fulfillmentText": response_text
    })

if __name__ == '__main__':
    app.run(debug=True)
