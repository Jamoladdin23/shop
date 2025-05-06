document.addEventListener("DOMContentLoaded", function (event) {
    const orderForm = document.getElementById("order-form");

    if (orderForm) {
        orderForm.addEventListener("submit", function (event) {
            event.preventDefault();

            let formData = new FormData(orderForm);

            fetch("/place_order/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      window.location.href = "/order_success/";
                  } else {
                      alert("Ошибка при оформлении заказа. Проверьте данные!");
                  }
              });
        });
    }
});
