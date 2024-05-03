from urllib import request
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
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