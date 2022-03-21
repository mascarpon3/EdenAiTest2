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

    def get_items(self):
        return CartItems.objects.filter(cart=self)

    def __str__(self):
        return f"{self.user}: {self.get_items()}"


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cart.user.username}: {self.product.name} ({self.quantity})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Cart.objects.create(user=instance)
