from django.shortcuts import render
from .models import Products

from django.shortcuts import render, redirect
from .forms import ProductForm

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