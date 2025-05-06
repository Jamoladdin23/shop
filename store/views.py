from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Cart, CartItem, Product, Category, Order, OrderItem
from .forms import CustomUserCreationForm, OrderForm
from django.contrib import messages
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'store/login.html'



def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.cart and cart_item.cart.user != request.user:
        return JsonResponse({'error': 'Нет доступа!'}, status=403)

    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')

        if new_quantity and new_quantity.isdigit() and int(new_quantity) > 0:
            cart_item.quantity = int(new_quantity)
            cart_item.save()
            return JsonResponse({'success': True, 'quantity': cart_item.quantity})

        return JsonResponse({'success': False, 'error': 'Неверное значение'}, status=400)



    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'}, status=400)


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    products = category.products.all()  # Получить все продукты в категории
    return render(request, 'store/category_detail.html', {'category': category, 'products': products})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_images = product.images.all()  # ✅ Получаем все фото продукта
    return render(request, 'store/product_detail.html', {'product': product, 'product_images': product_images})



from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from .models import Cart, CartItem, Product

def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = get_object_or_404(Product, id=product_id)

            # 📌 Проверяем, авторизован ли пользователь
            if request.user.is_authenticated:
                cart, _ = Cart.objects.get_or_create(user=request.user)
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                session_key = request.session.session_key

                cart, _ = Cart.objects.get_or_create(session_key=session_key)  # ✅ Корзина для анонимных

            # 📌 Добавляем товар в корзину
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return JsonResponse({"success": True, "message": "Товар добавлен в корзину!"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Некорректный запрос"})

# def add_to_cart(request, product_id):
#     if request.method == "POST":
#         try:
#             product = get_object_or_404(Product, id=product_id)
#             cart, created = Cart.objects.get_or_create(user=request.user)
#             cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#
#             if not created:
#                 cart_item.quantity += 1
#                 cart_item.save()
#
#             return redirect("cart_view")
#         except Exception as e:
#             return JsonResponse({"success": False, "error": str(e)})
#     # return redirect("cart_view")
#     return JsonResponse({"success": False, "error": "Некорректный запрос"})


def cart_view(request):
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)  # Создаём или получаем корзину
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        session_key = request.session.session_key

        cart, _ = Cart.objects.get_or_create(session_key=session_key)  # Корзина для анонимных

    # 📌 Получаем товары из корзины
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})



def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Удаляем товар из корзины
    cart_item.delete()

    return redirect('cart_view')


def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        CartItem.objects.filter(cart=cart).delete()
    return redirect('cart_view')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Выполняем вход
            messages.success(request, 'Вы успешно зарегистрировались! Теперь вы можете войти.')
            return redirect('product_list')

        else:
            messages.error(request, 'Ошибка регистрации. Проверьте введённые данные.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/signup.html', {'form': form})


@login_required
def place_order(request):
    if request.method == "POST":
        recipient_name = request.POST.get("recipient_name")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")

        if not recipient_name or not address or not phone_number:
            return JsonResponse({"success": False, "error": "Заполните все поля!"})

        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            return JsonResponse({"success": False, "error": "Корзина пуста!"})

        order = Order.objects.create(
            user=request.user,
            recipient_name=recipient_name,
            address=address,
            phone_number=phone_number
        )

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        cart_items.delete()
        return JsonResponse({"success": True})


def order_success(request):
    return render(request, 'order_success.html')


def payment_view(request):
    pass  # Заглушка, пока функционал не нужен
