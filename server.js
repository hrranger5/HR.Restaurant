document.getElementById("login-form").reset();
addEventListener("submit", function(event) {
    event.preventDefault();
    let username = document.getElementById("login-username").value;
    let password = document.getElementById("login-password").value;

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            alert("Login Successful!");
            window.location.href = "dashboard.html";  
        } else {
            alert("Invalid Credentials!");
        }
    })
    .catch(error => console.error("Error:", error));
});

document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault();
    let username = document.getElementById("signup-username").value;
    let password = document.getElementById("signup-password").value;

    fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
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
