from django.shortcuts import render
from .models import Products

from django.shortcuts import render, redirect
from .forms import ProductForm

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')   # redirect to product list
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


# Create your views here.

def index(request):
    product = Products.objects.all()
    return render(request, 'index.html', {'product': product})



# Custom pagination class
class ProductPagination(PageNumberPagination):
    page_size = 5  # default items per page
    page_size_query_param = 'page_size'  # allow client to set page size
    max_page_size = 50  # max allowed


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.all()

        # Filtering by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)

        # Filtering by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price and min_price.isdigit():
            queryset = queryset.filter(price__gte=min_price)
        if max_price and max_price.isdigit():
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
