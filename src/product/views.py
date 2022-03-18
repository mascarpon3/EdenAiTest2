from rest_framework.views import APIView
from rest_framework.response import Response
from product.serializers import ProductSerializer
from product.models import Product
from django.http import HttpResponse


class ProductsList(APIView):
    def get(self, request, format=None):
        if "sortby" in request.GET:
            if request.GET["sortby"] in ["price", "name"]:
                sortby = request.GET["sortby"]
            else:
                return HttpResponse(
                    f"sortby should be ether 'price' or 'name' not {request.GET['sortby']}",
                    status=400,
                )
        else:
            sortby = "name"

        products = Product.objects.all().order_by(sortby)

        if "department" in request.GET:
            products = products.filter(department__exact=request.GET["department"])

        if "maxprice" in request.GET:
            try:
                float(request.GET['maxprice'])
            except ValueError:
                return HttpResponse(
                    f"maxprice must be an integer or a float",
                    status=400,
                )
            products = products.filter(price__lte=request.GET["maxprice"])

        if "minprice" in request.GET:
            try:
                float(request.GET['minprice'])
            except ValueError:
                return HttpResponse(
                    f"mineprice must be an integer or a float",
                    status=400,
                )
            products = products.filter(price__gte=request.GET["minprice"])

        return Response(ProductSerializer(products, many=True).data)
