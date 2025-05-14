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
from werkzeug.utils import secure_filename




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

def send_otp_email(email, otp):
    try:
        msg = Message(
            subject="Password Reset OTP",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = f"Your OTP for password reset is: {otp}. It is valid for 10 minutes."
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        return False

@app.route('/')
def home():
    
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
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['user_role'] = user['role']  

            
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
    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    users = cursor.fetchone()[0]  # Access the first element of the tuple
    cursor.execute("SELECT COUNT(*) AS total_orders FROM orders")
    orders = cursor.fetchone()[0]  # Access the first element of the tuple
    
    cursor.close()
    conn.close()
    return render_template('admin_dashboard.html', 
                           total_users=users, 
                           total_orders=orders)

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

@app.route('/admin/reservations')
@admin_required
def admin_reservations():
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash("Admin access required.", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, person, phone, guests, date_time FROM reservations ORDER BY date_time DESC")
    rows = cursor.fetchall()
    conn.close()

    # Convert tuple rows to list of dictionaries
    reservations = []
    for row in rows:
        reservations.append({
            'id': row[0],
            'person': row[1],
            'phone': row[2],
            'guests': row[3],
            'date_time': row[4]
        })

    return render_template('reservations.html', reservations=reservations)

@app.route('/admin/reservations/cancel/<int:reservation_id>', methods=['POST'])
@admin_required
def cancel_reservation(reservation_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))
    conn.commit()
    conn.close()
    flash("Reservation cancelled successfully.", "success")
    return redirect(url_for('admin_reservations'))

def get_reservation_by_id(reservation_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservations WHERE id = %s", (reservation_id,))
    reservation = cursor.fetchone()
    cursor.close()
    conn.close()
    return reservation


@app.route('/admin/feedback')
@admin_required
def admin_feedback():
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash("Admin access required.", "danger")
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Join feedback with users to get feedback_text and user details
    query = """
        SELECT feedback.feedback_id, feedback.feedback_text, feedback.timestamp, users.username 
        FROM feedback
        JOIN users ON feedback.user_id = users.user_id
        ORDER BY feedback.timestamp DESC
    """
    cursor.execute(query)
    feedbacks = cursor.fetchall()
    conn.close()
    
    return render_template('feedback.html', feedbacks=feedbacks)
@app.route('/admin/feedback/delete/<int:feedback_id>', methods=['GET'])
@admin_required
def delete_feedback(feedback_id):
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash("Admin access required.", "danger")
        return redirect(url_for('login'))

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to delete the feedback entry
    cursor.execute("DELETE FROM feedback WHERE feedback_id = %s", (feedback_id,))
    conn.commit()  # Commit the changes to the database

    conn.close()

    # Flash success message and redirect back to the feedback page
    flash("Feedback deleted successfully.", "success")
    return redirect(url_for('admin_feedback'))  # Redirect to the feedback page

mock_db = {
    'admin': {
        'name': 'Hafsa',
        'email': 'hrranger555@gmail.com',
        'password': '$2b$12$hNLouuoztSjQeeu8/MbOWeVIk/ufxVjfZnLd2qirnnr...',  
        'profile_picture': 'default.jpg',  
        'status': 'active',
        'role': 'admin',
        'created_at': '2025-04-27 18:44:25'
    }
}

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/admin/setting', methods=['GET'])
def setting():
    # Get the admin data from mock DB
    admin = mock_db.get('admin')
    return render_template('setting.html', admin=admin)
@app.route('/admin/update-profile', methods=['POST'])
def update_profile():
    admin = mock_db.get('admin')
    name = request.form['name']
    email = request.form['email']
    password = request.form.get('password')  
    admin['name'] = name
    admin['email'] = email
    if password:
        admin['password'] = password  
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            admin['profile_picture'] = filename  
    flash("Profile updated successfully!", "success")
    return redirect(url_for('setting'))

@app.route('/user_dashboard')
def user_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    # 📦 1. Get user_id from the users table
    cursor.execute("SELECT user_id, email, phone FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return redirect(url_for('logout'))

    user_id = user['user_id']
    email = user['email']
    phone = user['phone']

    # 🧾 2. Fetch recent orders
    cursor.execute("""
        SELECT order_id,user_id, order_status, created_at
        FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 5
    """, (user_id,))
    recent_orders = cursor.fetchall()

    # Process recent orders
    if not recent_orders:
        recent_orders = [{
            'order_id': 'N/A',
            'user_id': ' ',
            'order_status': 'No Orders',
            'created_at': 'N/A',
            'status_color': 'secondary'
        }]
    else:
        for order in recent_orders:
            status = order['order_status']
            if status == 'Completed':
                order['status_color'] = 'success'
            elif status == 'Pending':
                order['status_color'] = 'warning'
            else:
                order['status_color'] = 'danger'

    # 📅 3. Fetch upcoming reservations
    cursor.execute("""
        SELECT date_time, guests
        FROM reservations
        WHERE person = %s
        ORDER BY date_time ASC
        LIMIT 5
    """, (username,))
    upcoming_reservations = cursor.fetchall()

    # Process upcoming reservations
    for res in upcoming_reservations:
        res['status'] = 'Confirmed'
        res['status_color'] = 'info'

    cursor.close()
    conn.close()

    # Render the template with the fetched data
    return render_template("user_dashboard.html",
                           username=username,
                           email=email,
                           phone=phone,
                           recent_orders=recent_orders,
                           upcoming_reservations=upcoming_reservations)

#----================-forgot password route===============-------

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            otp = generate_otp()
            expiry = datetime.now() + timedelta(minutes=10)
            cursor.execute("""
                INSERT INTO password_resets (user_id, otp, expires_at)
                VALUES (%s, %s, %s)
            """, (user['user_id'], otp, expiry))
            conn.commit()
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

#------------------ Assuming you have a function to get user details from the database----------
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
    otp = request.args.get('otp')  
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Verify OTP using password_resets
    cursor.execute("""
        SELECT user_id FROM password_resets 
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
            # ✅ Update user's password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute("""
                UPDATE users SET password_hash = %s WHERE user_id = %s
            """, (hashed_password, reset['user_id']))

            # ✅ Mark OTP as used
            cursor.execute("""
                UPDATE password_resets SET used = 1 WHERE otp = %s
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
            
            
            
            return redirect(url_for('reset_password', otp=otp))
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

#-----------------------------------Webhook Connection----------------------

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json(force=True)
        intent = req['queryResult']['intent']['displayName']

        logging.debug(f"Received intent: {intent}")
        
        if intent == 'Make Reservation':
            return make_reservation(req)
        elif intent == 'Order Tracking':
            return order_tracking(req)
        elif intent == 'AddToCart':
            return add_to_cart(req)
        elif intent == 'Place-Order':
            return place_order(req)
        elif intent == 'Feedback':
            return submit_feedback(req)
        elif intent == 'RegisterUser':
            return register_user(req)
        elif intent == 'Order Status':
            return get_order_status(req)
        
        else:
            return jsonify({'fulfillmentText': "Sorry, I couldn't understand your request."}), 400

    except Exception as e:
        logging.error(f"Error in webhook: {e}")
        return jsonify({'fulfillmentText': "Sorry, an error occurred. Please try again later."}), 500


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

def get_order_status(req):
    params = req.get("queryResult", {}).get("parameters", {})
    order_id = params.get("order_id")  # Directly extract without indexing
    email = params.get("email")  # Directly extract without indexing

    if not order_id or not email:
        return jsonify({
            'fulfillmentText': "Please provide both your order ID and email to check your order status."
        })

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Fixed query to join the 'orders' and 'users' tables
        cursor.execute("""
            SELECT o.order_status 
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            WHERE o.order_id = %s AND u.email = %s
        """, (order_id, email))
        
        result = cursor.fetchone()
        conn.close()

        if result:
            return jsonify({'fulfillmentText': f"Your order #{order_id} is currently '{result[0]}'."})
        else:
            return jsonify({'fulfillmentText': "Order not found or details are incorrect."})

    except Exception as e:
        print("Order status error:", e)
        return jsonify({'fulfillmentText': "Something went wrong while checking your order. Please try again."})

def make_reservation(req):
    from datetime import datetime
    import logging

    params = req.get("queryResult", {}).get("parameters", {})

    try:
        name = params.get("person", {}).get("name", "Guest")
        phone = params.get("phone", "N/A")
        num_guests = params.get("num_guests", 1)

        date_str = params.get("date", "")
        time_str = params.get("time", "")

        # Convert to datetime
        date_obj = parse_datetime(date_str)
        time_obj = parse_datetime(time_str)
        reservation_datetime = date_obj.replace(
            hour=time_obj.hour, minute=time_obj.minute
        )

        formatted_date = reservation_datetime.strftime("%Y-%m-%d")
        formatted_time = reservation_datetime.strftime("%I:%M %p")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert reservation
        cursor.execute(
            "INSERT INTO reservations (person, phone, guests, date_time) VALUES (%s, %s, %s, %s)",
            (name, phone, num_guests, reservation_datetime)
        )
        conn.commit()

        # ✅ Get the ID of the inserted reservation
        reservation_id = cursor.lastrowid

        response_text = (
            f"Thanks {name}, your table for {num_guests} guests is booked on "
            f"{formatted_date} at {formatted_time}. Your reservation ID is {reservation_id}. "
            f"We'll contact you at {phone}."
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
    feedback_text = parameters.get('feedback_text', '')
    user_id = parameters.get('user_id', '')

    # Validate that feedback and user_id are provided
    if not feedback_text:
        return jsonify({'fulfillmentText': "Please provide your feedback."})
    
    if not user_id:
        return jsonify({'fulfillmentText': "Please provide a valid user ID to submit feedback."})

    # Define lists for detecting positive and negative feedback
    negative_keywords = ['slow', 'cold', 'bad', 'poor', 'late', 'rude', 'unpleasant', 'worst', 'terrible', 'disappointing']
    positive_keywords = ['good', 'excellent', 'great', 'amazing', 'tasty', 'delicious', 'friendly', 'awesome', 'perfect', 'fast']

    # Determine the type of feedback (positive or negative)
    is_negative = any(word in feedback_text.lower() for word in negative_keywords)
    is_positive = any(word in feedback_text.lower() for word in positive_keywords)

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

        # Respond based on feedback sentiment
        if is_negative:
            response_text = "We're sorry your experience wasn't great. We’re working to improve and appreciate your feedback."
        elif is_positive:
            response_text = "Thank you! We're thrilled you had a good experience. Your feedback means a lot to us!"
        else:
            response_text = f"Thank you for your feedback! You said: {feedback_text}"

    except Exception as e:
        logging.error(f"Error submitting feedback: {str(e)}")
        response_text = f"Error submitting feedback: {e}"

    finally:
        cursor.close()
        conn.close()

    return jsonify({'fulfillmentText': response_text})

def handle_feedback(req):
    # Extract the query text to detect "register me" intent
    query_text = req.get('queryResult', {}).get('queryText', '').lower()

    # If the user says something like "OK" or "Register me"
    if "register me" in query_text or "ok" in query_text:
        return jsonify({
            'fulfillmentText': "Great! Let's get started with your registration. Please provide your name."
        })
    
    # Extract other parameters for feedback if needed (handling feedback intent)
    parameters = req.get('queryResult', {}).get('parameters', {})
    feedback_text = parameters.get('feedback_text', '')
    user_id = parameters.get('user_id', '')

    # If user is providing feedback, process it
    if feedback_text:
        return submit_feedback(req)

    return jsonify({
        'fulfillmentText': "Sorry, I didn't understand that. Can you please clarify?"
    })

import bcrypt

def register_user(req):
    cursor = None
    conn = None

    parameters = req.get('queryResult', {}).get('parameters', {})
    user_name = parameters.get('person', {}).get('name', '')
    user_email = parameters.get('email', '')
    user_password = parameters.get('password', '')

    if not user_name:
        return jsonify({'fulfillmentText': "Please provide your name."})
    if not user_email:
        return jsonify({'fulfillmentText': "Please provide your email."})
    if not user_password:
        return jsonify({'fulfillmentText': "Please provide a password."})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({'fulfillmentText': "This email is already registered. Please log in instead."})

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


        # Insert new user
        cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        """, (user_name, user_email, hashed_password))

        conn.commit()
        return jsonify({'fulfillmentText': f"🎉 Thank you {user_name}, you are successfully registered!"})

    except Exception as e:
        print("Error during registration:", e)  # Log the exception
        return jsonify({'fulfillmentText': f"⚠️ Error occurred during registration. Please try again later. Details: {str(e)}"})

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
