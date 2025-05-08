import pytest
from .models import Product, Category

@pytest.mark.django_db
def test_product_creation():
    category = Category.objects.create(name="Электроника")
    product = Product.objects.create(name="Ноутбук", category=category, price=1000, stock=10)

    assert product.name == "Ноутбук"
    assert product.price == 1000
    assert product.stock == 10
    assert product.is_available is True  # Доступен при наличии
