# 📦 Database Schema – HR.Restaurant Chatbot

This folder contains the SQL schema file exported from XAMPP's phpMyAdmin for the **restaurant_chatbot** database.

## 📁 Files Included

- **database_schema.sql**  
  Contains the full structure and sample data for:
  - `users` – stores customer and admin details
  - `admin` – manages superadmin credentials
  - `orders` and `order_items` – track customer orders and items
  - `menu_items` – the restaurant's digital menu
  - `reservations` – manages table bookings
  - `feedback` – collects user ratings and comments
  - `chat_sessions` – stores conversation history between users and the chatbot

## 🔗 Usage Instructions

1. Open **phpMyAdmin** in XAMPP
2. Create a new database named: `restaurant_chatbot`
3. Use the **Import** tab to upload and execute `database_schema.sql`
4. All necessary tables and sample data will be created automatically

## ⚙️ Features & Constraints

- Uses `InnoDB` engine and proper primary/foreign keys
- Includes ENUMs for statuses (e.g., `order_status`, `reservation status`)
- Supports chat history tracking
- Allows real-time integration with Flask backend & Dialogflow webhook

---

📌 This schema is an essential part of the HR.Restaurant chatbot system, designed to support real-time reservation, order, and feedback management.

