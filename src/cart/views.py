from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from account.utils import get_user_from_post_request
from cart.serializers import CartItemsSerializer
from cart.models import CartItems
from product.models import Product


class AddProductsToTheCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = CartItemsSerializer(data={
            "product": request.data["product_id"],
            "user": get_user_from_post_request(request).id,
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
        all_items = CartItems.objects.filter(user=get_user_from_post_request(request))
        return Response({"response": f"it's fine {all_items} for {all_items.compute_price}"})
