import unittest
from unittest import mock

from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from api import services
from api.models import Product, Cart, CartProduct
from api.serializers import ProductSerializer


class TestCartView(APITestCase):
    URL = reverse("cart")

    def setUp(self):
        self.product_1 = Product.objects.create(name="Rick", price=12, quantity=32, image="img")
        self.product_2 = Product.objects.create(name="Morty", price=153, quantity=42, image="img")
        self.product_3 = Product.objects.create(name="rick and morty", price=133, quantity=12, image="img")
        self.product_4 = Product.objects.create(name="Again rIck and morty", price=15.5, quantity=0, image="img")

    def test_add_to_cart(self):
        with self.assertRaisesRegexp(ValidationError, "product field missing or inconsistent"):
            self.client.post(self.URL)
        with self.assertRaisesRegexp(ValidationError, "product field missing or inconsistent"):
            self.client.post(self.URL, {"product": "nope"})
        with self.assertRaisesRegexp(ValidationError, "product field missing or inconsistent"):
            self.client.post(self.URL, {"product": -1})

        with self.assertRaisesRegexp(ValidationError, "quantity field missing or inconsistent"):
            self.client.post(self.URL, {"product": self.product_1.id})
        with self.assertRaisesRegexp(ValidationError, "product field missing or inconsistent"):
            self.client.post(self.URL, {"product": self.product_1.id, "quantity": "nope"})
        with self.assertRaisesRegexp(ValidationError, "product field missing or inconsistent"):
            self.client.post(self.URL, {"product": self.product_1.id, "quantity": -1})

        response = self.client.post(self.URL, {"product": self.product_1.id, "quantity": 5})

        try:
            cart = Cart.objects.first()
            CartProduct.objects.get(cart=cart, product=self.product_1, quantity=5)
        except Cart.DoesNotExist:
            self.fail("The cart hasn't been created")
        except CartProduct.DoesNotExist:
            self.fail("No CartProduct found for this product and this quantity")

        self.product_1.refresh_from_db()


if __name__ == "__main__":
    unittest.main()
