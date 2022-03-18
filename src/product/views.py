from rest_framework.views import APIView
from rest_framework.response import Response
from product.serializers import ProductSerializer
from product.models import Product


class ProductsList(APIView):
    def get(self, request, format=None):
        print(request.GET)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
