from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from product.models import Product
from cart.models import CartItems


class CartAddProducts(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name=f'cafetière',
            price=80,
            department="electromenager",
            stock=3,
        )
        Product.objects.create(
            name=f'vélo',
            price=600,
            department="sport",
            stock=1,
        )
        Product.objects.create(
            name=f"radio",
            price=60,
            department="electromenager",
            stock=2,
        )
        cls.user = User.objects.create(username="Eden")
        token = Token.objects.get(user__username='Eden')
        cls.headers = {'Authorization': 'Token ' + token.key}
        cls.api_client = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_add_one_product(self):
        url = 'http://localhost:8000/api/cart/add_products'
        data = {"product_id": 1, "quantity": 1}
        self.api_client.post(url, headers=self.headers, data=data)

        cart_items = CartItems.objects.get(user=self.user, product=Product(id=data["product_id"]))
        self.assertEqual(cart_items.quantity, 1)

    def test_add_one_product_and_another(self):
        url = 'http://localhost:8000/api/cart/add_products'
        data = {"product_id": 1, "quantity": 1}
        self.api_client.post(url, headers=self.headers, data=data)
        self.api_client.post(url, headers=self.headers, data=data)

        cart_items = CartItems.objects.get(user=self.user, product=Product(id=data["product_id"]))
        self.assertEqual(cart_items.quantity, 2)

    def test_add_Three_product(self):
        url = 'http://localhost:8000/api/cart/add_products'
        data = {"product_id": 1, "quantity": 3}
        self.api_client.post(url, headers=self.headers, data=data)

        cart_items = CartItems.objects.get(user=self.user, product=Product(id=data["product_id"]))
        self.assertEqual(cart_items.quantity, 3)

    def test_add_more_products_than_there_are(self):
        url = 'http://localhost:8000/api/cart/add_products'
        data = {"product_id": 1, "quantity": 12}
        response = self.api_client.post(url, headers=self.headers, data=data).content.decode("utf-8")
        expected = '{"stock":"you are trying to buy 12 cafetière(s) but we have only 3 left."}'
        self.assertEqual(expected, response)
