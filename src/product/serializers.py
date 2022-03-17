from rest_framework import serializers
from product.models import Product, Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer(many=False)

    class Meta:
        model = Product
        fields = '__all__'
