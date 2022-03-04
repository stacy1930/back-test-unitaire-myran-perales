import unittest
from unittest import mock

from django.urls import reverse
from rest_framework.test import APITestCase

from api.models import Product
from api.serializers import ProductSerializer


class TestProductsView(APITestCase):
    def setUp(self):
        self.product_1 = Product.objects.create(name="Rick", price=12, quantity=32, image="img")
        self.product_2 = Product.objects.create(name="Morty", price=153, quantity=42, image="img")
        self.product_3 = Product.objects.create(name="rick and morty", price=133, quantity=12, image="img")
        self.product_4 = Product.objects.create(name="Again rIck and morty", price=15.5, quantity=0, image="img")

    @mock.patch("api.views.services.check_rick_and_morty_characters")
    def test_list_all_products(self, mock_check_rick_and_morty_characters):
        url = reverse("products")

        response = self.client.get(url)
        expected_response = ProductSerializer(
            [self.product_1, self.product_2, self.product_3, self.product_4], many=True
        ).data
        self.assertEqual(response.data, expected_response)

        mock_check_rick_and_morty_characters.assert_called_once()
        # Assert called once in the test, to be sure I don't forget to un-comment it

    @mock.patch("api.views.services.check_rick_and_morty_characters")
    def test_filter_products(self, _):
        url = reverse("products")
        
        response = self.client.get(url, {"name": "Rick"})
        expected_response = ProductSerializer([self.product_1, self.product_3, self.product_4], many=True).data
        self.assertEqual(response.data, expected_response)

        response = self.client.get(url, {"price_max": 15.5})
        expected_response = ProductSerializer([self.product_1, self.product_4], many=True).data
        self.assertEqual(response.data, expected_response)

        response = self.client.get(url, {"price_min": 133})
        expected_response = ProductSerializer([self.product_2, self.product_3], many=True).data
        self.assertEqual(response.data, expected_response)

        response = self.client.get(url, {"available": True})
        expected_response = ProductSerializer([self.product_1, self.product_2, self.product_3], many=True).data
        self.assertEqual(response.data, expected_response)

        response = self.client.get(url, {"name": "Rick", "price_min": 10, "price_max": 100, "available": True})

        expected_response = ProductSerializer([self.product_1], many=True).data
        self.assertEqual(response.data, expected_response)

    def test_retrieve_product(self):
        url = reverse("products_detail", args=[self.product_1.id])

        response = self.client.get(url)

        expected_response = ProductSerializer(self.product_1).data
        self.assertEqual(response.data, expected_response)


if __name__ == "__main__":
    unittest.main()
