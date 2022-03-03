from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api.models import Product, Cart
from api.serializers import ProductSerializer, CartSerializer


class ProductView(ListCreateAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        pass


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'id'


class CartView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_url_kwarg = 'id'
