function updateOrderStatus(orderId, status) {
    let token = localStorage.getItem("token");

    fetch(`http://127.0.0.1:5000/update_order_status/${orderId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    })
    .catch(error => console.error("Error:", error));
}
