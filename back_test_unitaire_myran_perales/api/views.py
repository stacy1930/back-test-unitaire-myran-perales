from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response

from api import services
from api.models import Product, Cart
from api.serializers import ProductSerializer, CartSerializer


class ProductView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # to avoid bug, even though it shouldn't happen. Except with Stacy. Because she's too strong for us mere mortals

    def get(self, request, *args, **kwargs):
        services.check_rick_and_morty_characters()

        products = Product.objects.all()

        name = request.query_params.get("name")
        if name:
            products = products.filter(name__icontains=name)

        price_min = request.query_params.get("price_min")
        if price_min:
            products = products.filter(price__gte=price_min)

        price_max = request.query_params.get("price_max")
        if price_max:
            products = products.filter(price__lte=price_max)

        available_only = request.query_params.get("available")
        if available_only:
            products = products.filter(quantity__gt=0)

        data = self.get_serializer(products, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'id'


class CartView(CreateAPIView, RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")

        try:
            product = Product.objects.get(id=product_id)
        except (Product.DoesNotExist, ValueError, TypeError):
            raise ValidationError("product field missing or inconsistent")

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            raise ValidationError("quantity field missing or inconsistent")

        cart = services.get_or_create_cart()
        services.add_to_cart(cart, product, quantity)

        data = self.get_serializer(cart).data
        
        return Response(data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        cart = services.get_or_create_cart()
        data = self.get_serializer(cart).data
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get("product")

        try:
            product = Product.objects.get(id=product_id)
        except (Product.DoesNotExist, ValueError, TypeError):
            raise ValidationError("product field missing or inconsistent")

        cart = services.get_or_create_cart()
        services.remove_from_cart(cart, product)

        data = self.get_serializer(cart).data

        return Response(data, status=status.HTTP_200_OK)
