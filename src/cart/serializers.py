from rest_framework import serializers
from django.db.models import Q

from product.serializers import ProductSerializer
from cart.models import Cart, CartItems


class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ('id', 'cart', 'product', 'quantity')

    def save(self):
        existing_cart_items = CartItems.objects.filter(
            Q(product=self.validated_data["product"].id) & Q(cart=self.validated_data['cart'].id)
        )
        if existing_cart_items:
            assert len(existing_cart_items) == 1
            cart_items = CartItems.objects.get(
                product=self.validated_data["product"].id, cart=self.validated_data['cart'].id
            )
            cart_items.quantity += self.validated_data['quantity']
        else:
            cart_items = CartItems(
                cart=self.validated_data['cart'],
                product=self.validated_data['product'],
                quantity=self.validated_data['quantity'],
            )

        if self.validated_data['product'].stock < cart_items.quantity:
            raise serializers.ValidationError({
                "stock": f"you are trying to buy {cart_items.quantity} "
                f"{self.validated_data['product'].name}(s) but we have only "
                f"{self.validated_data['product'].stock} left."
            })

        cart_items.save()
        response = f"{cart_items.quantity} {self.validated_data['product']}(s) successfully added to the cart."

        return response, cart_items.quantity


class FormCartItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItems
        fields = ('id', 'cart', 'product', 'quantity')


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"
