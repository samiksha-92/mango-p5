from django.contrib import admin
from . models import Products

# Register your models here.

@admin.register(Products)
class ProductsModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price', 'category', 'product_image']
