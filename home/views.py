from urllib import request
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views import View
from  .models import Products

# Create your views here.
def index(request):
    return render (request,'home/index.html')

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
    def get (self,request,title):
        product_queryset_category_titles = Products.objects.filter(title=title)
        product_individual_category_title = None
        if product_queryset_category_titles.exists():
            product_individual_category_title = product_queryset_category_titles[0].category

        context = {
            'title': title,
            'product_queryset_category_titles': product_queryset_category_titles,
            'product_individual_category_title': product_individual_category_title,
        }

        return render (request, 'home/category.html',context)






