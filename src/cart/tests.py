from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from product.models import Product, Discount
from cart.models import Cart, CartItems


class CartComputePrice(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username="Eden"
        )
        cls.cart = Cart.objects.create(user=cls.user)
        discount = Discount.objects.create(
            ratio=0.1,
            how_many_bought=3,
            how_many_offered=2,
        )
        product_1 = Product.objects.create(
            name=f'cafetière',
            price=80,
            department="electromenager",
            stock=6,
            discount=discount
        )
        product_2 = Product.objects.create(
            name=f'corde à sauter',
            price=12,
            department="sport",
            stock=20,
            discount=discount
        )
        cls.cart_items_1 = CartItems.objects.create(
            cart=cls.cart,
            product=product_1,
            quantity=4,
        )
        cls.cart_items_2 = CartItems.objects.create(
            cart=cls.cart,
            product=product_2,
            quantity=10,
        )

    def test_compute_nb_free_products_1(self):
        result_nb_free_products = self.cart_items_1.compute_nb_free_products()
        expected = 1

        self.assertEqual(expected, result_nb_free_products)

    def test_compute_nb_free_products_2(self):
        result_nb_free_products = self.cart_items_2.compute_nb_free_products()
        expected = 4

        self.assertEqual(expected, result_nb_free_products)

    def test_compute_price(self):
        result_price = self.cart.compute_price()
        expected = ((4 - 1) * 80 + (10 - 4) * 12) * (1 - 0.1)

        self.assertEqual(expected, result_price)


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

        cls.url = 'http://localhost:8000/api/cart/add_products'
        cls.cart = Cart.objects.create(user=User.objects.create(username="Eden"))
        token = Token.objects.get(user__username='Eden')
        cls.headers = {'Authorization': 'Token ' + token.key}
        cls.api_client = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_add_one_product(self):
        data = {"product_id": 1, "quantity": 1}
        self.api_client.post(self.url, headers=self.headers, data=data)

        cart_items = CartItems.objects.get(cart=self.cart, product=Product(id=data["product_id"]))
        self.assertEqual(cart_items.quantity, 1)

    def test_add_one_product_and_another(self):
        data = {"product_id": 1, "quantity": 1}
        self.api_client.post(self.url, headers=self.headers, data=data)
        self.api_client.post(self.url, headers=self.headers, data=data)

        cart_items = CartItems.objects.get(cart=self.cart, product=Product(id=data["product_id"]))
        self.assertEqual(cart_items.quantity, 2)

    def test_add_Three_product(self):
        data = {"product_id": 1, "quantity": 3}
        self.api_client.post(self.url, headers=self.headers, data=data)

        cart_items = CartItems.objects.get(cart=self.cart, product=Product(id=data["product_id"]))
        self.assertEqual(cart_items.quantity, 3)

    def test_add_more_products_than_there_are(self):
        data = {"product_id": 1, "quantity": 12}
        response = self.api_client.post(self.url, headers=self.headers, data=data).content.decode("utf-8")

        expected = '{"stock":"you are trying to buy 12 cafetière(s) but we have only 3 left."}'
        self.assertEqual(expected, response)
