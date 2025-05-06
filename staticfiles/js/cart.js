document.addEventListener("DOMContentLoaded", function () {
    const addToCartButtons = document.querySelectorAll(".add-to-cart");

    addToCartButtons.forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.dataset.productId;
            fetch("/place_order/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            }
        }).then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text); });
            }
            return response.json();
        }).then(data => {
            if (data.success) {
                window.location.href = "/order_success/";
            } else {
                alert("Ошибка: " + data.error);
            }
        }).catch(error => {
            console.error("Ошибка сервера:", error);
            alert("Что-то пошло не так. Проверьте консоль.");
        });
    });
});
