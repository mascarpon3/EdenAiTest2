from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def compute_price(self):
        product_price = Product.obejct.get(id=self.product)
        return product_price * self.qatity

    def __str__(self):
        return f"{self.user.username}: {self.product.name}"
