document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    fetch("backend/login.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Login Successful!");
            window.location.href = "dashboard.html"; // Redirect to Dashboard
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

    fetch("backend/signup.php", {
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
