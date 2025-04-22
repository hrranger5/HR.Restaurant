//  Login Function
document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let email = document.getElementById("login-email").value;
    let password = document.getElementById("login-password").value;

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            alert("Login Successful!");
            window.location.href = "/dashboard";  
        } else {
            alert("Invalid Credentials!");
        }
    })
    .catch(error => console.error("Error:", error));
});

// Signup Function
document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let username = document.getElementById("signup-username").value;
    let email = document.getElementById("signup-email").value;
    let password = document.getElementById("signup-password").value;

    fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "User registered successfully!") {
            alert("Signup Successful! Please login.");
            window.location.href = "login.html";
        } else {
            alert("Signup Failed. Username may already exist.");
        }
    })
    .catch(error => console.error("Error:", error));
});

// Logout Function
function logout() {
    localStorage.removeItem("token");
    alert("Logged out successfully!");
    window.location.href = "/login";
}

// Fetch Dashboard Data (Only If Logged In)
document.addEventListener("DOMContentLoaded", function() {
    if (window.location.pathname === "/dashboard") {
        let token = localStorage.getItem("token");
        
        if (!token) {
            alert("Unauthorized! Please login.");
            window.location.href = "/login";
            return;
        }

        fetch("http://127.0.0.1:5000/dashboard", {
            method: "GET",
            headers: { "Authorization": "Bearer " + token }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Unauthorized") {
                alert("Access Denied!");
                window.location.href = "/login";
            } else {
                document.getElementById("dashboard-welcome").innerText = `Welcome, ${data.user.username}`;
            }
        })
        .catch(error => console.error("Error:", error));
    }
});

// Place Order Function
document.addEventListener("DOMContentLoaded", () => {
    const orderButtons = document.querySelectorAll(".menu-item .btn-primary");

    orderButtons.forEach(button => {
        button.addEventListener("click", () => {
            const itemCard = button.closest(".menu-item");
            const itemName = itemCard.querySelector(".card-title").textContent;
            const itemPrice = itemCard.querySelector(".card-text").textContent.match(/\d+/)[0];

            fetch('/place_order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    item: itemName,
                    price: itemPrice
                })
            })
            .then(response => {
                if (response.ok) {
                    alert("Order placed successfully for: " + itemName);
                } else {
                    alert("Failed to place order. Please login.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error placing order.");
            });
        });
    });
});

//  Make Reservation Function
document.getElementById("reservation-form").addEventListener("submit", function(event) {
    event.preventDefault();

    let token = localStorage.getItem("token");
    if (!token) {
        alert("Please login to make a reservation.");
        return;
    }

    let reservationData = {
        user_id: 1, // Replace with actual logged-in user ID
        num_guests: document.getElementById("num-guests").value,
        reservation_time: document.getElementById("reservation-time").value
    };

    fetch("http://127.0.0.1:5000/make_reservation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify(reservationData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error("Error:", error));
});
