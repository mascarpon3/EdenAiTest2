from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from cart.serializers import CartItemsSerializer


class AddProductToTheCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        key = request.META["HTTP_AUTHORIZATION"].replace("Token ", "")
        user_id = Token.objects.get(key=key).user.id
        serializer = CartItemsSerializer(data={
            "product_id": request.data["product_id"],
            "user_id": user_id,
            "quantity": request.data["quantity"]
        })
        if serializer.is_valid():
            data = {
                "response": "so far so good.",
            }
        else:
            data = serializer.errors

        return Response(data)
