import unittest
from unittest import mock

from rest_framework.test import APITestCase

from api import services
from api.models import Product


class TestServices(APITestCase):

    @mock.patch("api.services.get_request_to_rick_and_morty_api")
    @mock.patch("api.services.check_character")
    def test_check_rick_and_morty_characters(self, mock_check_character, mock_get_request_to_rick_and_morty_api):
        mock_get_request_to_rick_and_morty_api.side_effect = [
            {
                "info": {"next": "link to page 2"},
                "results": [
                    {"id": 1, "name": "Probably Rick"},
                    {"id": 2, "name": "Morty, I assume"}
                ]
            },
            {
                "info": {"next": "link to page 3"},
                "results": [
                    {"id": 3, "name": "Mrs Doubtfire"},
                    {"id": 4, "name": "Who care, it's 4:30 am"}
                ]
            },
            {
                "info": {"next": None},
                "results": [
                    {"id": 5, "name": "Probably Rick again, cause why not?"}
                ]
            }
        ]

        services.check_rick_and_morty_characters()

        expected_get_request_to_rick_and_morty_api_calls = [
            mock.call('https://rickandmortyapi.com/api/character/'),
            mock.call('link to page 2'),
            mock.call('link to page 3')
        ]
        self.assertEqual(
            mock_get_request_to_rick_and_morty_api.mock_calls,
            expected_get_request_to_rick_and_morty_api_calls,
            msg=f"mock_get_request_to_rick_and_morty_api called with arguments "
                f"{mock_get_request_to_rick_and_morty_api.mock_calls}"
        )

        expected_check_character_calls = [
            mock.call({'id': 1, 'name': 'Probably Rick'}),
            mock.call({'id': 2, 'name': 'Morty, I assume'}),
            mock.call({'id': 3, 'name': 'Mrs Doubtfire'}),
            mock.call({'id': 4, 'name': "Who care, it's 4:30 am"}),
            mock.call({'id': 5, 'name': 'Probably Rick again, cause why not?'})
        ]
        self.assertEqual(
            mock_check_character.mock_calls,
            expected_check_character_calls,
            msg=f"mock_check_character called with arguments {mock_check_character.mock_calls}"
        )

    @mock.patch("api.services.random.uniform", return_value=12.5)
    def test_check_character(self, _):
        Product.objects.create(name="Rick", price=10, image="some img", rick_and_morty_id=None, quantity=15)
        Product.objects.create(name="Morty", price=2, image="some img", rick_and_morty_id=42, quantity=8)

        character_info = {"name": "Morty", "image": "some img", "id": 42}
        services.check_character(character_info)

        self.assertEqual(Product.objects.count(), 2)  # check no product has been created

        character_info = {"name": "Rick", "image": "some img", "id": 666}
        services.check_character(character_info)

        self.assertEqual(Product.objects.count(), 3)
        try:
            new_product = Product.objects.get(rick_and_morty_id=666)
            self.assertEqual(new_product.name, "Rick")
            self.assertEqual(new_product.price, 12.5)
            self.assertEqual(new_product.quantity, 20),
            self.assertEqual(new_product.image, "some img")
        except Product.DoesNotExist:
            self.fail("We should have a product with r&m id of 666. Not found in DB")


if __name__ == "__main__":
    unittest.main()
