from django.test import TestCase
from product.models import Product


class GetProductsListtest(TestCase):
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

    def test_filter_by_department_1(self):
        response = self.client.get('http://localhost:8000/api/all_products?department=sport')
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(ordered_response_names, ["vélo"])

    def test_filter_by_department_2(self):
        response = self.client.get('http://localhost:8000/api/all_products?department=electromenager')
        ordered_response_names = [p["name"] for p in response.json()]
        self.assertEqual(ordered_response_names, ["cafetière", "radio"])
