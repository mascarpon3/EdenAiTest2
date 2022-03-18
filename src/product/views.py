from rest_framework.views import APIView
from rest_framework.response import Response
from product.serializers import ProductSerializer
from product.models import Product
from django.http import HttpResponse


class ProductsList(APIView):
    def get(self, request, format=None):

        if "sortby" not in request.GET:
            products = Product.objects.all()
        elif request.GET["sortby"] not in ["price", "name"]:
            return HttpResponse(
                f"sortby should be ether 'price' or 'name' not {request.GET['sortby']}",
                status=400,
            )
        else:
            products = Product.objects.all().order_by(request.GET["sortby"])

        return Response(ProductSerializer(products, many=True).data)
