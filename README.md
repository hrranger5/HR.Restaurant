# HR.++Restaurant Chatbot 🏨🤖

A restaurant-based NLP chatbot using Dialogflow, Flask, and MySQL for table reservations, order-taking, menu navigation, and customer support.

## Features
- ✅ **Table Reservation** – Users can book, modify, or cancel reservations.
- ✅ **Menu Navigation** – Users can explore the restaurant's menu.
- ✅ **Order Placement** – Users can place and modify food orders.
- ✅ **Customer Support** – Includes FAQs, order tracking, and feedback.

## Technologies Used
- **NLP Engine:** DialogFlow
- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Integration:** Webhooks (for chatbot-backend connection)

## Work Completed So Far
1. **Dialogflow Setup & Intents**
   - Defined four main use cases: Table Reservation, Menu Navigation, Order Placement, and Customer Support.
   - Configured intents for each use case:
     - Reservation: Booking, Modifications, Cancellation.
     - Menu: Menu Exploration.
     - Orders: Adding/Removing items.
     - Support: FAQs, Feedback, Order Tracking, Live Chat.
   - Integrated Dialogflow agent with webhook.

2. **Backend Development (Flask & MySQL)**
   - Setup Flask server to handle chatbot responses.
   - Created APIs for:
     - Handling reservations (add, modify, cancel).
     - Fetching menu details from MySQL database.
     - Processing and modifying orders.
     - Customer support queries (tracking orders, FAQs, feedback).
   - Integrated MySQL with Flask using XAMPP.

3. **Database Structure (MySQL with XAMPP)**
   - Designed and implemented MySQL database:
     - `reservations` table for booking details.
     - `menu` table storing food items.
     - `orders` table tracking placed orders.
     - `customer_support` table for FAQs and feedback.
   - Established database connectivity with Flask.

4. **Frontend Development**
   - Developed a basic website using HTML, CSS, and JavaScript.
   - Integrated chatbot UI with Dialogflow API.
   - Created user-friendly interfaces for:
     - Reservation form.
     - Menu display.
     - Order placement.
     - Customer support section.

## Next Steps
- Complete chatbot UI enhancements.
- Implement user authentication and session management.
- Deploy backend and database on a cloud server.
- Optimize responses and improve NLP accuracy.
- Conduct testing and debugging.

---
