from django.contrib import admin
from . models import Products,Customer,Cart

# Register your models here.

@admin.register(Products)
class ProductsModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price', 'category', 'product_image']



@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city', 'state', 'zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']  

class OrderPlacedModelAdmin(admin.ModelAdmin): 
    list_display=['id','user','customer','product','quantity','ordered_date','status','payments']