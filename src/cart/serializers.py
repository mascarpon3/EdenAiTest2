from rest_framework import serializers
from cart.models import CartItems


class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ('user_id', 'product_id', 'quantity')
