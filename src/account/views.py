from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from account.serializers import RegisterSerializer


class UserRegistrationList(APIView):

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            data = {
                "response": "new user successfully registered.",
                "email": user.email,
                "username": user.username,
                "token": token,
            }
        else:
            data = serializer.errors

        return Response(data)
