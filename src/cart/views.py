from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from account.utils import get_user_from_post_request
from cart.serializers import FormCartItemsSerializer, CartItemsSerializer, CartSerializer
from cart.models import Cart, CartItems
from product.models import Product


class AddProductsToTheCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            cart = Cart.objects.get(user=get_user_from_post_request(request), validated=False)
        except:
            cart = Cart.objects.create(user=get_user_from_post_request(request))

        serializer = CartItemsSerializer(data={
            "product": request.data["product_id"],
            "cart": cart.id,
            "quantity": int(request.data["quantity"]),
        })

        if serializer.is_valid():
            response, quantity = serializer.save()
            data = {
                "response": response,
                "product": Product.objects.get(id=request.data["product_id"]).name,
                "quantity": quantity
            }
        else:
            data = serializer.errors

        return Response(data)


class ValidateCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            cart = Cart.objects.get(user=get_user_from_post_request(request), validated=False)
        except:
            return Response({"cart": "cart is empty"})

        cart_items = CartItems.objects.filter(cart=cart)
        cart.validated = True
        cart.save()

        return Response({
            "cart": CartSerializer(cart).data,
            "cart_items": FormCartItemsSerializer(cart_items, many=True).data,
        })
