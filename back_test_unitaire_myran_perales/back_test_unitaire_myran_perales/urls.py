"""back_test_unitaire_myran_perales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views import static

from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products', ProductView.as_view(), name="products"),
    path('api/products/<int:id>', ProductDetailView.as_view(), name="products_detail"),
    path('api/carts/', CartView.as_view(), name="carts"),
    path('api/carts/<int:id>', CartDetailView.as_view(), name="carts_detail"),
]
