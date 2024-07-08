"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from classes.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    def test_product_check_quantity(self, product):
        assert product.check_quantity(1) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(999) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        product.buy(5)
        assert product.quantity == 995
        product.buy(95)
        assert product.quantity == 900
        product.buy(900)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:

    def test_add_product(self, cart, product):
        cart.add_product(product, 1)
        assert cart.products[product] == 1
        cart.add_product(product, 2)
        assert cart.products[product] == 3
        cart.add_product(product, 45)
        assert cart.products[product] == 48
        cart.add_product(product, 900)
        assert cart.products[product] == 948
        cart.add_product(product, 0)
        assert cart.products[product] == 948

    def test_remove_product(self, cart, product):
        cart.add_product(product, 3)
        cart.remove_product(product, 1)
        assert cart.products[product] == 2
        cart.remove_product(product, 2)
        assert product not in cart.products

    def test_remove_product_all(self, cart, product):
        cart.add_product(product, 10)
        cart.remove_product(product, 10)
        assert product not in cart.products
        cart.add_product(product, 1001)
        cart.remove_product(product, 1001)
        assert product not in cart.products

    def test_dict_clear(self, cart, product):
        cart.add_product(product, 1)
        cart.clear()
        assert len(cart.products) == 0
        cart.add_product(product, 10)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 3)
        assert cart.get_total_price() == 300
        cart.add_product(product, 1)
        assert cart.get_total_price() == 400
        cart.remove_product(product, 3)
        assert cart.get_total_price() == 100
        cart.remove_product(product, 1)
        assert cart.get_total_price() == 0

    def test_buy(self, cart, product):
        cart.add_product(product, 2)
        cart.buy()
        assert product.quantity == 998
        assert len(cart.products) == 0

    def test_buy_exceeding_limit(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            cart.buy()
        cart.add_product(product, 10000)
        with pytest.raises(ValueError):
            cart.buy()
