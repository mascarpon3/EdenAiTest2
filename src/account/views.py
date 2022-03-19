from rest_framework.views import APIView
from rest_framework.response import Response
from account.serializers import RegisterSerializer


class UserRegistrationList(APIView):

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                "response": "new user successfully registered.",
                "email": user.email,
                "username": user.username
            }
        else:
            data = serializer.errors

        return Response(data)
