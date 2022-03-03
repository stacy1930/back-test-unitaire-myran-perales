import random

from rest_framework import status

from api import constants as c

import requests

from api.models import Product


def get_request_to_rick_and_morty_api(path):
    r = requests.get(path)
    if r.status_code != status.HTTP_200_OK:
        raise  # figure out which exception to raise
    result = r.json()
    return result


def check_character(character_info):
    name = character_info["name"]
    image = character_info["image"]
    api_id = character_info["id"]
    try:
        Product.objects.get(id=api_id)
    except Product.DoesNotExist:
        Product.objects.create(
            name=name, image=image, rick_and_morty_id=api_id, quantity=20, price=round(random.uniform(8.0, 70.5), 2)
        )


def check_rick_and_morty_characters():
    path = c.RICK_AND_MORTY_ENDPOINT + c.RICK_AND_MORTY_CHARACTERS
    while path:
        api_response = get_request_to_rick_and_morty_api(path)
        path = api_response["info"]["next"]
        for character in api_response["results"]:
            check_character(character)
