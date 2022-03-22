from django.db import models
from django.contrib.auth.models import User

from product.models import Product

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    validated = models.BooleanField(default=False)
    datetime_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s cart: {self.compute_price()}€"

    def get_all_items(self):
        return CartItems.objects.filter(cart=self)

    def compute_price(self):
        return sum([items.compute_price() for items in self.get_all_items()])


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}): {self.compute_price()}€"

    def compute_price(self):
        discount = self.product.discount
        return (self.quantity - self.compute_nb_free_products()) * (1 - discount.ratio) * self.product.price

    def compute_nb_free_products(self):
        discount = self.product.discount
        pack_size = discount.how_many_bought + discount.how_many_offered
        nb_free_products_1 = int(self.quantity / pack_size) * discount.how_many_offered
        nb_free_products_2 = max(self.quantity % pack_size - discount.how_many_bought, 0)
        return nb_free_products_1 + nb_free_products_2


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Cart.objects.create(user=instance)
