from django.db import models


class Discount(models.Model):
    ratio = models.FloatField()
    how_many_bought = models.IntegerField(default=1)
    how_many_offered = models.IntegerField(default=0)


class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    department = models.CharField(max_length=128)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
