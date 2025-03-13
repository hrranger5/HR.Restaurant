// JavaScript to handle menu item addition dynamically
document.addEventListener("DOMContentLoaded", function () {
    const menuSection = document.querySelector(".menu-items");
    
    const menuItems = [
        { name: "Pizza", price: "$12" },
        { name: "Burger", price: "$8" },
        { name: "Pasta", price: "$10" }
    ];

    menuItems.forEach(item => {
        const div = document.createElement("div");
        div.classList.add("menu-item");
        div.innerHTML = `<h3>${item.name}</h3><p>${item.price}</p>`;
        menuSection.appendChild(div);
    });
});

// Form validation for reservation
document.getElementById("reservation-form").addEventListener("submit", function (event) {
    event.preventDefault();
    alert("Reservation Successful!");
});
