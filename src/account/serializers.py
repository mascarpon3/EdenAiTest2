from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {'password2': {'write_only': True}}

    def save(self):
        if "email" not in self.validated_data:
            self.validated_data['email'] = None
        user = User.objects.create_user(
            self.validated_data['username'],
            self.validated_data['email'],
            self.validated_data['password']
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "password must match."})
        else:
            user.set_password(password)
            user.save()
            return user
