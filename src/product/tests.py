from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from product.models import Product


class GetProductsListtest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name=f'cafetière',
            price=80,
            department="electromenager",
        )
        Product.objects.create(
            name=f'vélo',
            price=600,
            department="sport",
        )
        Product.objects.create(
            name=f"radio",
            price=60,
            department="electromenager",
        )

        User.objects.create(username="Eden")
        token = Token.objects.get(user__username='Eden')
        cls.headers = {'Authorization': 'Token ' + token.key}
        cls.api_client = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_order_by_name(self):
        url = 'http://localhost:8000/api/products?sortby=name'
        response = self.api_client.get(url, headers=self.headers)
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(
            ordered_response_names, ["cafetière", "radio", "vélo"]
        )

    def test_order_by_price(self):
        url = 'http://localhost:8000/api/products?sortby=price'
        response = self.api_client.get(url, headers=self.headers)
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(
            ordered_response_names, ["radio", "cafetière", "vélo"]
        )

    def test_filter_by_department_1(self):
        url = 'http://localhost:8000/api/products?department=sport'
        response = self.api_client.get(url, headers=self.headers)
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(ordered_response_names, ["vélo"])

    def test_filter_by_department_2(self):
        url = 'http://localhost:8000/api/products?department=electromenager'
        response = self.api_client.get(url, headers=self.headers)
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(ordered_response_names, ["cafetière", "radio"])

    def test_filter_by_min_price(self):
        url = 'http://localhost:8000/api/products?minprice=120'
        response = self.api_client.get(url, headers=self.headers)
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(ordered_response_names, ["vélo"])

    def test_filter_by_max_price(self):
        url = 'http://localhost:8000/api/products?maxprice=120'
        response = self.api_client.get(url, headers=self.headers)
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(ordered_response_names, ["cafetière", "radio"])

    def test_filter_by_min_and_max_price(self):
        url = 'http://localhost:8000/api/products?minprice=70&maxprice=120'
        response = self.api_client.get(url, headers=self.headers)
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(ordered_response_names, ["cafetière"])

    def test_filter_by_price_and_department(self):
        url = 'http://localhost:8000/api/products?maxprice=70&department=electromenager'
        response = self.api_client.get(url, headers=self.headers)
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(ordered_response_names, ["radio"])

    def test_order_by_price_and_filter_by_department(self):
        url = 'http://localhost:8000/api/products?sortby=price&department=electromenager'
        response = self.api_client.get(url, headers=self.headers)
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(ordered_response_names, ["radio", "cafetière"])
