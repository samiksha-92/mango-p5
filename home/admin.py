from django.contrib import admin
from . models import Products,Customer

# Register your models here.

@admin.register(Products)
class ProductsModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price', 'category', 'product_image']



@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city', 'state', 'zipcode']