from urllib import request

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views import View
from  .models import Products,Customer,Cart
from .forms import CustomerProfileForm,CustomerRegistrationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist



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


# def address(request):
#     address = Customer.objects.filter(user = request.user)
#     context = {
#         'address' : address
#     }
#     return render(request,'home/address.html',context)

from django.contrib.auth.decorators import login_required

@login_required
def address(request):
    print("User:", request.user)  # Debugging statement
    address = Customer.objects.filter(user=request.user)
    print("Addresses:", address)  # Debugging statement
    context = {
        'address': address
    }
    return render(request, 'home/address.html', context)


    
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


# def add_to_cart(request):
#     user = request.user
#     product_id = request.GET.get('prod_id')
#     product = Products.objects.get(id= product_id)
#     Cart.objects.create(user=user, product=product)
#     return redirect("/cart")


from django.db.models import Q

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Products.objects.get(id=product_id)
    
    # Check if the product already exists in the user's cart
    existing_cart_item = Cart.objects.filter(user=user, product=product).first()
    
    if existing_cart_item:
        # If the product already exists, increase the quantity
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        # If the product doesn't exist, create a new cart entry
        Cart.objects.create(user=user, product=product, quantity=1)
    
    return redirect("/cart")

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        
        # Retrieve the product
        try:
            product = Products.objects.get(id=prod_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=400)
        
        # Check if the cart item already exists for the specified product and user
        try:
            cart_item = Cart.objects.get(product=product, user=user)
            # If the cart item exists, update the quantity
            cart_item.quantity += 1
            cart_item.save()
        except Cart.DoesNotExist:
            # Return an error if the cart item does not exist
            return JsonResponse({'error': 'Cart item does not exist for the specified product and user'}, status=400)
        
        # Calculate amount and total amount
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40
        
        # Prepare data to be sent in the JSON response
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render (request, 'home/addtocart.html', locals())

class checkout(View):
    def get(self,request):
        user = request.user
        addresses = Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)  
        total_amount = 0
        for item in cart_items:
            value = item.quantity * item.product.discounted_price
            total_amount += value
        total_amount += 40
        context = {
            'user': user,
            'addresses': addresses,
            'cart_items': cart_items,
            'total_amount': total_amount
        }
        return render(request, 'home/checkout.html',context)
   



# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET.get('prod_id')
#         user = request.user
        
#         # Retrieve the product
#         try:
#             product = Products.objects.get(id=prod_id)
#         except Product.DoesNotExist:
#             return JsonResponse({'error': 'Product does not exist'}, status=400)
        
#         # Check if the cart item already exists for the specified product and user
#         try:
#             cart_item = Cart.objects.get(product=product, user=user)
#             # If the cart item exists, update the quantity
#             cart_item.quantity += 1
#             cart_item.save()
#         except Cart.DoesNotExist:
#             # If the cart item does not exist, create a new cart item with quantity 1
#             Cart.objects.create(product=product, user=user, quantity=1)
        
#         # Calculate amount and total amount
#         cart = Cart.objects.filter(user=user)
#         amount = sum(p.quantity * p.product.discounted_price for p in cart)
#         totalamount = amount + 40
        
#         # Prepare data to be sent in the JSON response
#         data = {
#             'quantity': cart_item.quantity if cart_item else 1,  # Return 1 if cart item does not exist
#             'amount': amount,
#             'totalamount': totalamount
#         }
#         return JsonResponse(data)

            






def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')

        try:
            # Attempt to get the Cart object for the given product ID and user
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        except Cart.MultipleObjectsReturned:
            # Handle the case where multiple Cart objects are returned
            # Log the error or return an appropriate response
            return JsonResponse({'error': 'Multiple Cart objects found for the specified product and user'})

        except Cart.DoesNotExist:
            # Handle the case where the Cart object does not exist
            return JsonResponse({'error': 'Cart object does not exist for the specified product and user'})

        # Ensure quantity is not reduced below 0
        if c.quantity > 0:
            c.quantity -= 1
            c.save()
        else:
            # Delete the cart item if the quantity reaches 0
            c.delete()
        
        # Calculate amount and total amount
        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40
        
        # Prepare data to be sent in the JSON response
        data = {
            'quantity': c.quantity if c.quantity > 0 else 0,  # Return 0 if quantity is 0 after decrement
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)



def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)             



