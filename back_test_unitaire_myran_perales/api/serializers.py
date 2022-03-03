from rest_framework import serializers

from api.models import Product, Cart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "products"]
