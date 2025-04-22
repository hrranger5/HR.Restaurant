# 🍽️ Restaurant Chatbot Project – HR.Restaurant

This repository contains the full source code for the restaurant chatbot project. It integrates a Flask backend, frontend interface, MySQL database, and Dialogflow for chatbot interactions.

---

## 🚀 Features

- **Make Reservation:** Customers can make, update, or cancel table reservations.
- **Menu Navigation:** Explore available menu items through the chatbot.
- **Place Order:** Order food directly via chatbot with modification options.
- **Customer Support:** Track orders, access FAQs, give feedback, and live chat support.

---

## 💻 Source Code – Folder Overview

### 📁 `src/`
The main folder containing backend, frontend, and Dialogflow integration code.

#### Key Files:

- `app.py`  
  Flask backend application that handles routes, sessions, and connects to MySQL.

- `fetchdata.py`  
  Includes logic for retrieving data (e.g., orders, feedback, reservations) from the MySQL database.

- `requirements.txt`  
  Contains a list of required Python libraries (Flask, bcrypt, mysql-connector-python, etc.).

---

### 📂 Folder Structure

#### 📁 `templates/`
- `index.html`  
  Homepage with chatbot interface, reservation form, and menu. Connected to CSS and JS.

#### 📁 `static/`
Static assets like CSS and JavaScript.

- 📁 `css/`
  - `styles.css` — Main styling for buttons, layout, forms.

- 📁 `js/`
  - `script.js` — Handles form logic (login/signup).
  - `server.js` — AJAX or additional backend interaction.

---

### 🔗 Application Flow

#### Backend Flow

1. Dialogflow receives user input.
2. Sends intent to Flask (`app.py`) via webhook.
3. Flask calls `fetchdata.py` to query MySQL.
4. Responds back with chatbot message via Dialogflow.

#### Frontend Flow

1. `index.html` is rendered by Flask.
2. CSS applies design from `styles.css`.
3. JS files provide client-side interactivity (form validation, AJAX, etc.).
4. Flask handles form data and user sessions.

---

## 🧾 Database Schema

### 📁 `schema/`
- `database_schema.sql`  
  SQL file containing all required table definitions: users, reservations, orders, feedback, etc.

  Includes foreign key relationships and data types aligned with Dialogflow fulfillment requirements.

---

## 📄 Documentation

### 📁 `docs/`

- `Fall 2024_CS619_10108_3.docx` — Project handout and initial problem statement.
- `SRS Document` — Software Requirements Specification outlining functional and non-functional requirements.
- `Design Document` — Architecture, flow diagrams, and interface design for the system.
- `Prototype Screenshots` — Visual demonstration of chatbot interaction and frontend.

---

## 👩‍💻 Author Info

- **Name**: Hafsa  
- **Student ID**: BC210414048  
- **Course**: CS619 – Final Year Project (Fall 2024)  
- **Project Title**: HR.Restaurant – AI Chatbot for Restaurant Management

---

📌 *This chatbot aims to streamline restaurant operations using NLP and web technologies, ensuring ease of reservation, ordering, and customer support via intelligent automation.*


