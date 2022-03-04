import unittest

from rest_framework.test import APITestCase

from api.models import Product, Cart, CartProduct


class TestModelDisplay(APITestCase):
    def test_product_display(self):
        product = Product.objects.create(name="Rick", image="img", price=12.5, quantity=45, rick_and_morty_id=666)

        self.assertEqual(str(product), f"({product.id}) Rick - cost : 12.5€ - 45 left")

    def test_cart_display(self):
        product_1 = Product.objects.create(name="Rick", image="img", price=12.5, quantity=45, rick_and_morty_id=666)
        product_2 = Product.objects.create(name="Morty", image="img", price=6, quantity=12, rick_and_morty_id=42)
        cart = Cart.objects.create()
        CartProduct.objects.create(cart=cart, product=product_1, quantity=5)
        CartProduct.objects.create(cart=cart, product=product_2, quantity=7)

        self.assertEqual(str(cart), f"Cart {cart.id} (contains 2 products)")

    def test_cart_product_display(self):
        product = Product.objects.create(name="Rick", image="img", price=12.5, quantity=45, rick_and_morty_id=666)
        cart = Cart.objects.create()
        cart_product = CartProduct.objects.create(cart=cart, product=product, quantity=5)

        self.assertEqual(str(cart_product), "5 Rick(s) in cart")


if __name__ == "__main__":
    unittest.main()
