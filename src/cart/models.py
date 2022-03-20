from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class CartItems(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()

    def compute_price(self):
        return self.price

    def __str__(self):
        return self.user + " - " + self.product
