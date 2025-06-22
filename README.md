# HR.Restaurant 🍽️

An intelligent restaurant chatbot system powered by **Python (Flask)**, **MySQL**, and **Dialogflow**. This project enables customers to interact with the restaurant through a natural language interface for reservations, order placements, menu navigation, and customer support — all accessible via a responsive web platform.



---

## 📌 Features

- 🤖 **Dialogflow Chatbot Integration**
  - Make,or cancel reservations
  - Explore the restaurant menu
  - Place and update orders
  - Track orders, give feedback, FAQs

- 🧠 **NLP-based Interactions** (via Dialogflow)
- 🗂️ **Admin Dashboard** for managing users, orders, reservations, and feedback
- 🔐 **Authentication System**
  - Signup / Login
  - JWT-based session handling
  - Password update (with or without JWT)
- 🗃️ **MySQL Database Integration**

---

## 🛠️ Technologies Used

| Layer        | Tech Stack                         |
|--------------|------------------------------------|
| Frontend     | HTML, CSS, Bootstrap, JavaScript   |
| Backend      | Python (Flask), Flask-JWT          |
| NLP Engine   | Dialogflow                         |
| Database     | MySQL (via XAMPP)                  |
| Tools        | JWT, XAMPP, GitHub        |

---

## 🗂️ Project Structure

```
HR.Restaurant/
│
├── src/
│   ├── static/                # Static files (CSS, JS, etc.)
│   ├── template/              # HTML templates (index, login, admindashboard,base,feedback,orders,signup,updatepassword,update profile,reservation ,userdashboard etc.)
│   ├── app.py                 # Main Flask backend application
│   ├── fetchdata.py           # Database operations and utility functions
│
├── database/
│   └── restaurant.sql         # MySQL schema for the project
│
├── doc/
│   ├── SRS.pdf                # Software Requirements Specification
│   └── DesignDoc.pdf          # System Design Document
│
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## ⚙️ How to Run Locally

### 1. **Clone the Repository**

```bash
git clone https://github.com/hrranger5/HR.Restaurant.git
cd HR.Restaurant/src
```

### 2. **Create Virtual Environment and Activate**

```bash
python -m venv venv
venv\Scripts\activate   # For Windows
```

### 3. **Install Dependencies**

```bash
pip install -r ../requirements.txt
```

### 4. **Set Up MySQL Database**

- Open XAMPP and start Apache & MySQL.
- Open `phpMyAdmin` and create a database named: `restaurant_chatbot`
- Import the SQL file located at: `/database/restaurant_chatbot.sql`

### 5. **Run the Application**

```bash
python app.py
```

### 6. **Visit in Browser**

```bash
http://localhost:5000
```

---

## 🤖 Dialogflow Intents

| Use Case           | Intents                                                           |
|--------------------|-------------------------------------------                        |
| Make Reservation   | Make Reservation,Reservation Confirmation, Cancel_Reservation     |
| Menu Navigation    | Show Menu                                                      |
| Place Order        | place-order, order-status  ,add to cart                                           |
| Customer Support   | FAQs, Feedback, Track Order                                       |

---

## 📚 Project Documentation

| Document Name            | Description                                      | Location                     |
|--------------------------|--------------------------------------------------|------------------            |
| **SRS (Software Requirements Specification)** | Functional and non-functional requirements | `doc/SRS.pdf` |
| **Design Document**      | System architecture and design details           | `doc/DesignDoc.pdf`          |
| **FinalReport**          | FYP detail                                       | `doc/FinalReport.pdf`        |

---

## 👤 Author

- **Name:** Hafsa  
- **Roll No:** BC210414048  
- **Project Type:** Final Year Project (FYP)  
- **Domain:** NLP-based Chatbot System  
- **Platform:** Web  

---

## 🚀 Future Enhancements

- OTP-based password reset
- Email/SMS confirmation for reservations
- Admin analytics dashboard
- Mobile app interface

---

## 📬 Contact

For feedback or collaboration:  
📧 Email: `hrranger555@gmail.com` 
---

## 📜 License

This project is licensed under the MIT License.  
© 2025 Hafsa – All rights reserved.
