import unittest

from django.urls import reverse
from rest_framework.test import APITestCase

from api.models import Product, Cart, CartProduct
from api.serializers import CartSerializer


class TestCartView(APITestCase):
    URL = reverse("cart")

    def setUp(self):
        self.product_1 = Product.objects.create(name="Rick", price=12, quantity=32, image="img")
        self.product_2 = Product.objects.create(name="Morty", price=153, quantity=42, image="img")
        self.product_3 = Product.objects.create(name="rick and morty", price=133, quantity=12, image="img")
        self.product_4 = Product.objects.create(name="Again rIck and morty", price=15.5, quantity=0, image="img")

    def test_add_to_cart(self):
        # check product parameter
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.URL, {"product": "nope"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.URL, {"product": -1})
        self.assertEqual(response.status_code, 400)

        # check quantity parameter
        response = self.client.post(self.URL, {"product": self.product_1.id})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.URL, {"product": self.product_1.id, "quantity": "nope"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.URL, {"product": self.product_1.id, "quantity": -1})
        self.assertEqual(response.status_code, 400)

        # check adding
        response = self.client.post(self.URL, {"product": self.product_1.id, "quantity": 5})
        self.assertEqual(response.status_code, 200)

        try:
            cart = Cart.objects.first()
            CartProduct.objects.get(cart=cart, product=self.product_1, quantity=5)
        except Cart.DoesNotExist:
            self.fail("The cart hasn't been created")
        except CartProduct.DoesNotExist:
            self.fail("No CartProduct found for this product and this quantity")

        self.product_1.refresh_from_db()
        self.assertEqual(self.product_1.quantity, 27)

        expected_response = CartSerializer(cart).data
        self.assertEqual(response.data, expected_response)

    def test_retrieve_cart(self):
        cart = Cart.objects.create()
        CartProduct.objects.create(cart=cart, product=self.product_1, quantity=6)
        CartProduct.objects.create(cart=cart, product=self.product_3, quantity=12)

        response = self.client.get(self.URL)
        expected_response = CartSerializer(cart).data
        self.assertEqual(response.data, expected_response)

    def test_remove_from_cart(self):
        cart = Cart.objects.create()
        CartProduct.objects.create(cart=cart, product=self.product_1, quantity=23)
        CartProduct.objects.create(cart=cart, product=self.product_3, quantity=6)

        # check product parameter
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 400)

        response = self.client.delete(self.URL, {"product": "nope"})
        self.assertEqual(response.status_code, 400)

        response = self.client.delete(self.URL, {"product": -1})
        self.assertEqual(response.status_code, 400)

        response = self.client.delete(self.URL, {"product": self.product_3.id})
        self.assertEqual(response.status_code, 200)

        self.product_3.refresh_from_db()
        self.assertEqual(self.product_3.quantity, 18)
        self.assertFalse(CartProduct.objects.filter(cart=cart, product=self.product_3).exists())
        self.assertTrue(CartProduct.objects.filter(cart=cart, product=self.product_1).exists())

        expected_response = CartSerializer(cart).data

        self.assertEqual(response.data, expected_response)


if __name__ == "__main__":
    unittest.main()
