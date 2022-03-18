from django.test import TestCase
from product.models import Product, Discount


class GetProductsListtest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name=f'cafetière',
            price=80,
        )
        Product.objects.create(
            name=f'vélo',
            price=600,
        )
        Product.objects.create(
            name=f"radio",
            price=60,
        )

    def test_order_by_name(self):
        response = self.client.get('http://localhost:8000/api/all_products?sortby=name')
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(
            ordered_response_names,
            ["cafetière", "radio", "vélo"]
        )

    def test_order_by_price(self):
        response = self.client.get('http://localhost:8000/api/all_products?sortby=price')
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(
            ordered_response_names,
            ["radio", "cafetière", "vélo"]
        )