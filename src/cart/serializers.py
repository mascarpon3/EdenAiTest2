from rest_framework import serializers
from cart.models import CartItems
from product.models import Product


class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ('user', 'product', 'quantity')

    def save(self):

        if self.validated_data['product'].stock < self.validated_data['quantity']:
            raise serializers.ValidationError({
                "stock": f"you are strying to buy {self.validated_data['quantity']} "
                f"{self.validated_data['product'].name}(s) but we have only "
                f"{self.validated_data['product'].stock} left."
            })

        cart_items = CartItems(
            self.validated_data['user'].id,
            self.validated_data['product'].id,
            self.validated_data['quantity']
        )

        cart_items.save()
