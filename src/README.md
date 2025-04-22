# Restaurant Chatbot Project

# 💻 Source Code – HR.Restaurant Chatbot

This folder contains the full source code for the restaurant chatbot project, including the Flask backend, frontend files, and integration with Dialogflow.
This is a chatbot built for restaurant management, which includes features like reservations, menu navigation, and order placement.

## Features:

- **Make Reservation:** Customers can make reservations.
- **Menu Navigation:** Customers can explore menu items.
- **Place Order:** Customers can place orders from the menu.
- **Customer Support:** Chat support for inquiries, including tracking orders and FAQs.
- 
## 📁 Files Included
- `app.py`  
  Main backend script to run the web server, route chatbot requests, and connect with the MySQL database.
- `fetchdata.py`  
  Contains logic for MySQL queries such as retrieving orders, reservations, and feedback.
- `requirements.txt`  
  List of Python dependencies (e.g., Flask, mysql-connector-python, bcrypt, jwt).
 - `database_schema.sql
   contain all database tables which are connect through fullfillment of dialogflow 

## 📂 Folder Structure

### `templates/`
- Contains the HTML templates used by Flask to render pages.
  - `index.html`  
    Main homepage that dynamically displays content like the menu, reservation form, and chatbot interface. It connects with CSS and JavaScript for styling and interactivity.
### `static/`
This folder contains static files like CSS, JavaScript, and images that are referenced by HTML templates.
#### `static/css/`
- `styles.css`  
  The primary stylesheet for the project. It provides the styles for various components, such as buttons, forms, and layouts. It's linked to `index.html` for a consistent design across the site.
#### `static/js/`
- `script.js`  
  Contains the JavaScript code for client-side functionality, including handling the logic for login, signup forms, and interactions with the Flask backend. 
- `server.js`  
  Additional script for server-related operations if needed for backend/frontend communication or specific tasks like AJAX requests.

### `requirements.txt`

- Python dependencies for the project, such as Flask, mysql-connector-python, bcrypt, jwt, etc.

## 🔗 Frontend Flow

1. The homepage (`index.html`) is served by Flask.
2. The CSS from `static/css/styles.css` is applied to ensure the page has the desired layout and styling.
3. JavaScript files (`static/js/script.js`, `server.js`) provide interactivity, such as handling login and signup forms, as well as other frontend interactions.
4. The backend communicates with the frontend via forms and AJAX requests, which interact with the Flask routes defined in `app.py`.

---

📌 All frontend logic, including the forms and JavaScript interactions, is integrated with the backend system for handling user actions like login and signup.


