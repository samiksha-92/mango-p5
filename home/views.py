from urllib import request

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views import View
from  .models import Products
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.shortcuts import redirect


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
    


def success_page(request):
    return render(request, 'home/success.html')



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {
            'form': form,
        }
        return render (request,'home/customerregistration.html',context)
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! You registered successfully")
            return redirect('success-page')  # Redirect to the success page
        else:
            messages.error(request,"Invalid Input Data")
            context = {
            'form' : form
            }
            return render(request,'home/customerregistration.html',context)
        return render(request,'home/customerregistration.html') 



    

# class CategoryTitle(View):
#     def get(self, request, title):
#         print("Title:", title)



