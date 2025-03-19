function trackOrder() {
    let token = localStorage.getItem("token");
    let orderId = document.getElementById("orderId").value;

    fetch(`http://127.0.0.1:5000/order_status/${orderId}`, {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("orderStatus").innerText = "Order Status: " + data.order_status;
    })
    .catch(error => console.error("Error:", error));
}
