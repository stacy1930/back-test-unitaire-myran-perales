import functools
import random

from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException

from api import constants as c

import requests

from api.models import Product, Cart, CartProduct


def get_request_to_rick_and_morty_api(path):
    r = requests.get(path)
    if r.status_code != status.HTTP_200_OK:
        raise APIException(f"Rick and Morty API responded with status {r.status_code}")  # figure out which exception to raise
    result = r.json()
    return result


def check_character(character_info):
    name = character_info["name"]
    image = character_info["image"]
    api_id = character_info["id"]
    try:
        Product.objects.get(rick_and_morty_id=api_id)
    except Product.DoesNotExist:
        Product.objects.create(
            name=name, image=image, rick_and_morty_id=api_id, quantity=20, price=round(random.uniform(8.0, 70.5), 2)
        )


@functools.lru_cache(maxsize=None)
def check_rick_and_morty_characters():
    path = c.RICK_AND_MORTY_ENDPOINT + c.RICK_AND_MORTY_CHARACTERS
    while path:
        api_response = get_request_to_rick_and_morty_api(path)
        path = api_response["info"]["next"]
        for character in api_response["results"]:
            check_character(character)


def get_or_create_cart():
    if Cart.objects.count() > 0:
        cart = Cart.objects.first()
    else:
        cart = Cart.objects.create()

    return cart


def add_to_cart(cart, product, quantity):
    if product.quantity < quantity:
        raise ValidationError("The asked quantity for this product is too high")

    # maybe add a transaction.atomic
    try:
        cart_product = CartProduct.objects.get(cart=cart, product=product)
        cart_product.quantity += quantity
        cart_product.save()
    except CartProduct.DoesNotExist:
        CartProduct.objects.create(cart=cart, product=product, quantity=quantity)

    product.quantity -= quantity
    product.save()


def remove_from_cart(cart, product):
    try:
        cart_product = CartProduct.objects.get(cart=cart, product=product)
    except CartProduct.DoesNotExist:
        raise ValidationError("This product was not in the cart")

    product.quantity += cart_product.quantity
    product.save()
    cart_product.delete()
