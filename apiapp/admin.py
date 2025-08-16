from django.contrib import admin
from .models import  Products

# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ('name',)
    list_filter = ('category',)

admin.site.register(Products, ProductsAdmin)
