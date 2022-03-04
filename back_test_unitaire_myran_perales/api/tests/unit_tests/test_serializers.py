import json
import unittest

from rest_framework.test import APITestCase

from api.models import Product, Cart, CartProduct
from api.serializers import ProductSerializer, CartProductSerializer, CartSerializer


class TestSerializers(APITestCase):
    def test_product_serializer(self):
        product = Product.objects.create(
            name="Rick", image="some img link", quantity=12, price=55.99, rick_and_morty_id=42
        )

        expected_value = {
            "id": product.id,
            "name": "Rick",
            "image": "some img link",
            "quantity": 12,
            "price": 55.99,
            "rick_and_morty_id": 42
        }

        serializer = ProductSerializer(product).data
        self.assertEqual(serializer, expected_value)

    def test_cart_product_serializer(self):
        product = Product.objects.create(
            name="Rick", image="some img link", quantity=12, price=55.99, rick_and_morty_id=42
        )
        cart = Cart.objects.create()
        cart_product = CartProduct.objects.create(cart=cart, product=product, quantity=66)

        expected_value = {
            "product": {
                "id": product.id,
                "name": "Rick",
                "image": "some img link",
                "quantity": 12,
                "price": 55.99,
                "rick_and_morty_id": 42
            },
            "quantity": 66
        }

        serializer = CartProductSerializer(cart_product).data

        self.assertEqual(serializer, expected_value)

    def test_cart_serializer(self):
        product_1 = Product.objects.create(
            name="Rick", image="some img link", quantity=12, price=55.99, rick_and_morty_id=42
        )
        product_2 = Product.objects.create(
            name="Morty", image="some other link", quantity=42, price=12.5, rick_and_morty_id=666
        )
        cart = Cart.objects.create()
        CartProduct.objects.create(cart=cart, product=product_1, quantity=10)
        CartProduct.objects.create(cart=cart, product=product_2, quantity=8)

        expected_value = {
            "id": cart.id,
            "products": [
                {
                    "product": {
                        "id": product_1.id,
                        "name": "Rick",
                        "image": "some img link",
                        "quantity": 12,
                        "price": 55.99,
                        "rick_and_morty_id": 42
                    },
                    "quantity": 10
                },
                {
                    "product": {
                        "id": product_2.id,
                        "name": "Morty",
                        "image": "some other link",
                        "quantity": 42,
                        "price": 12.5,
                        "rick_and_morty_id": 666
                    },
                    "quantity": 8
                }
            ]
        }

        serializer = CartSerializer(cart).data

        self.assertEqual(serializer, expected_value)


if __name__ == "__main__":
    unittest.main()
