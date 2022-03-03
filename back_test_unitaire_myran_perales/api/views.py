from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from api.models import Product, Cart
from api.serializers import ProductSerializer, CartSerializer
from api.services import check_rick_and_morty_characters


class ProductView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()  # to avoid bug, even though it shouldn't happen. Except with Stacy. Because she's too strong for us mere mortals

    def get(self, request, *args, **kwargs):
        # check_rick_and_morty_characters()

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


class CartView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        products = request.data.get("products")
        for product_detail in products:
            pass


class CartDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_url_kwarg = 'id'
