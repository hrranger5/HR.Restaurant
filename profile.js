document.getElementById("profile-form").addEventListener("submit", function(event) {
    event.preventDefault();

    let token = localStorage.getItem("token");

    fetch("/update_profile", {
        method: "PUT",
        headers: { "Content-Type": "application/json", "Authorization": "Bearer " + token },
        body: JSON.stringify({
            name: document.getElementById("name").value,
            email: document.getElementById("email").value
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("updateMessage").innerText = data.message;
    })
    .catch(error => console.error("Error:", error));
});
