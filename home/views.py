from urllib import request

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views import View
from  .models import Products,Customer
from .forms import CustomerProfileForm,CustomerRegistrationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm


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
            messages.warning(request,"Invalid Input Data")
            context = {
            'form' : form
            }
            return render(request,'home/customerregistration.html',context)
        return render(request,'home/customerregistration.html') 



    




class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        context = {
            'form' : form
        }
        return render(request,'home/profile.html',context)

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data.get('name', '')  # Use get() method to safely access the value
            locality = form.cleaned_data.get('locality', '')
            city = form.cleaned_data.get('city', '')
            mobile = form.cleaned_data.get('mobile', '')
            state = form.cleaned_data.get('state', '')
            zipcode = form.cleaned_data.get('zipcode', '')

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Profile saved")
        else:
            messages.warning(request,"Invalid Input Data")    
        context = {'form' : form}
        return render(request,'home/profile.html',context)


def address(request):
    address = Customer.objects.filter(user = request.user)
    context = {
        'address' : address
    }
    return render(request,'home/address.html',context)

    
class updateAddress(View):
    def get(self,request,pk):
        addr = Customer.objects.get (pk=pk)
        form = CustomerProfileForm(instance=addr)
        context = {
            'form' : form
        }
        return render(request,'home/updateaddress.html',context)

    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            addr = Customer.objects.get(pk=pk)
            addr.name = form.cleaned_data['name']
            addr.locality = form.cleaned_data['locality']
            addr.city = form.cleaned_data['city']
            addr.mobile = form.cleaned_data['mobile']
            addr.state = form.cleaned_data['state']
            addr.zipcode = form.cleaned_data['zipcode']
            addr.save()
            messages.success(request,"Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")













