document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    fetch("http://127.0.0.1:5001/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Login Successful!");
            localStorage.setItem("token", data.token); // Store JWT token
            window.location.href = "dashboard.html";
        } else {
            alert("Invalid Credentials");
        }
    });
});

document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const name = document.getElementById("signup-name").value;
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;
    
    fetch("http://127.0.0.1:5001/profile", {
        method: "GET",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("profile-name").innerText = data.name;
        document.getElementById("profile-email").innerText = data.email;
    });
    
    fetch("http://127.0.0.1:5001/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Signup Successful! Please login.");
            window.location.href = "login.html";
        } else {
            alert("Signup Failed. Email already exists.");
        }
    });
});

function sendMessageToChatbot() {
    const userMessage = document.getElementById("chat-input").value;
    if (!userMessage.trim()) return;

    const token = localStorage.getItem("token"); // Retrieve JWT token
    if (!token) {
        alert("You need to login first.");
        return;
    }

    fetch("http://127.0.0.1:5001/dialogflow", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("chat-output").innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;
        document.getElementById("chat-output").innerHTML += `<p><strong>Bot:</strong> ${data.reply}</p>`;
        document.getElementById("chat-input").value = "";
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Session expired. Please login again.");
        localStorage.removeItem("token");
        window.location.href = "login.html";
    });
}
