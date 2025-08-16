from django.shortcuts import render
from .models import Products

from django.shortcuts import render, redirect
from .forms import ProductForm

# from rest_framework.generics import ListAPIView
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Product
# from .serializers import ProductSerializer


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

            # return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
