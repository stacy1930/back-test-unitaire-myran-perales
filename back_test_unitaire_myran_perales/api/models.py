from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=500, null=False)
    price = models.FloatField()
    image = models.CharField(max_length=5000, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    rick_and_morty_id = models.PositiveIntegerField(null=True, blank=True)  # None if the product is ours and not R&M

    def __str__(self):
        return f"({self.id}) {self.name} - cost : {self.price}€ - {self.quantity} left"


class Cart(models.Model):
    products = models.ManyToManyField(Product, through="CartProduct")

    def __str__(self):
        return f"Cart {self.id} (contains {self.products.count()} products)"


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.quantity} {self.product.name}(s) in cart"
