from django.test import TestCase
from django.contrib.auth.models import User
import ast


BASE_URL = 'http://localhost:8000/api/account/signup?'


class GetProductsListtest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="Eden",
            password='123sOlEil',
            email="eden.test@hello.wolrd",
        )

    def test_password_dont_match(self):
        result = self.client.post(
            "http://localhost:8000/api/account/signup",
            data={
                "username": "Pascale",
                "password": "123",
                "password2": "124",
            }
        ).content
        expected = b'{"password":"password must match."}'

        self.assertEqual(expected, result)

    def test_username_already_exist(self):
        result = self.client.post(
            "http://localhost:8000/api/account/signup",
            data={
                "username": "Eden",
                "password": "123",
                "password2": "123",
            }
        ).content
        expected = b'{"username":["A user with that username already exists."]}'
        self.assertEqual(expected, result)

    def test_new_user_successuflly_register(self):
        result = ast.literal_eval(
            self.client.post(
                "http://localhost:8000/api/account/signup",
                data={
                    "username": "Charles",
                    "password": "123",
                    "password2": "123",
                    "email": "charles.test@hello.world"
                }
            ).content.decode("utf-8")
        )["response"]
        expected = "new user successfully registered."
        self.assertEqual(expected, result)

        user = User.objects.get(username="Charles")
        self.assertEqual(user.email, "charles.test@hello.world")
