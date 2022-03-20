from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from cart.serializers import CartItemsSerializer
from product.models import Product


class AddProductToTheCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        key = request.META["HTTP_AUTHORIZATION"].replace("Token ", "")
        user_id = Token.objects.get(key=key).user.id
        serializer = CartItemsSerializer(data={
            "product": request.data["product_id"],
            "user": user_id,
            "quantity": request.data["quantity"]
        })
        if serializer.is_valid():
            serializer.save()
            product = Product.objects.get(id=request.data["product_id"])
            data = {
                "response": f"{request.data['quantity']} {product}(s) successfully added to the cart.",
                "product": product.name,
                "quantity": request.data["quantity"]
            }
        else:
            data = serializer.errors

        return Response(data)
