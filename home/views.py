from urllib import request
from django.db.models import F
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views import View
from  .models import Products

# Create your views here.
def index(request):
    return render (request,'home/index.html')

def about(request):
    return render (request,'home/about.html')    


class CategoryView(View):
    def get(self,request,category):
        context = {
            'category' : category,
            'product_queryset' : Products.objects.filter(category=category),
            'title' : Products.objects.filter(category=category).values('title'),
            
        }
        
        return render(request,'home/category.html',context)


class ProductDetail(View):
    def get (self,request,pk):
        product = get_object_or_404(Products,pk=pk)
        context = {'product' : product}
        
        return render(request,'home/productdetail.html', context)


class CategoryTitle(View):
    def get(self, request, category):
        sort_by = request.GET.get('sort_by')
        products = Products.objects.filter(title=category)
    
        if sort_by == 'price_low':
            products = products.order_by('discounted_price')
        elif sort_by == 'price_high':
            products = products.order_by('-discounted_price')
        elif sort_by == 'color':
            products = products.order_by('color')  # Assuming there's a 'color' field in your model
    
        context ={
            'category' : category,
            'product_queryset' :products
        }

        return render(request, 'home/category.html', context)
    

    

# class CategoryTitle(View):
#     def get(self, request, title):
#         print("Title:", title)



