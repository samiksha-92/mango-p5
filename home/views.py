from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
def index(request):
    return render (request,'home/index.html')

class CategoryView(View):
    def get(self,request,category):
        context = {
            'category' : category,
        }
        return render(request,'home/category.html',context)