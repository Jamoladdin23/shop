document.addEventListener("DOMContentLoaded", function () {
    const addToCartButtons = document.querySelectorAll(".add-to-cart");

    addToCartButtons.forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.dataset.productId;
//            console.log("Добавление товара:", productId); // Проверка


            fetch(`/cart/add/product/${productId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json"
                }
            })
            .then(() => {
                location.href = "/cart/"; // ✅ Вместо JSON просто открываем корзину
            })
            .then(data => {
               if (data.success) {
                  alert("Товар добавлен в корзину!");
                  location.reload(); // Перезагружаем страницу
              } else {
                  alert("Ошибка: " + data.error);
              }
            }).catch(error => console.error("Ошибка в fetch:", error));
        });
    });
});
