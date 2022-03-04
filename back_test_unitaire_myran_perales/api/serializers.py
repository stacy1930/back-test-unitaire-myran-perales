from rest_framework import serializers

from api.models import Product, Cart, CartProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = ["product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    @staticmethod
    def get_products(obj):
        cart_products = CartProduct.objects.filter(cart=obj)
        return CartProductSerializer(cart_products, many=True).data

    class Meta:
        model = Cart
        fields = ["id", "products"]
