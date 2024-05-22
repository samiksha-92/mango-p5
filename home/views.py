from urllib import request

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from  .models import Products,Customer,Cart,Payment,OrderPlaced
from .forms import CustomerProfileForm,CustomerRegistrationForm,ProductForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
import razorpay
from django.conf import settings




# Create your views here.

def index(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        context = {
            'totalitem' : totalitem
        } 
    return render (request,'home/index.html',context)


def about(request):
    return render (request,'home/about.html')    

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,category):
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        context = {
            'category' : category,
            'product_queryset' : Products.objects.filter(category=category),
            'title' : Products.objects.filter(category=category).values('title'),
            'totalitem' : totalitem
            
        }
        
        return render(request,'home/category.html',context)

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get (self,request,pk):
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        product = get_object_or_404(Products,pk=pk)
        context = {'product' : product,
        'totalitem': totalitem}
        
        return render(request,'home/productdetail.html', context)

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self, request, category):
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
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
            'product_queryset' :products,
            'totalitem': totalitem,
        } 

        return render(request, 'home/category.html', context)
    


def success_page(request):
    return render(request, 'home/success.html')


@method_decorator(login_required,name='dispatch')
class CustomerRegistrationView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        context = {
            'form': form,
            'totalitem' : totalitem
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


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        context = {
            'form' : form,
            'totalitem' : totalitem,
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



@login_required
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
    print("User:", request.user)  # Debugging statement
    address = Customer.objects.filter(user=request.user)
    print("Addresses:", address)  # Debugging statement
    context = {
        'address': address,
        'totalitem' :totalitem
    }
    return render(request, 'home/address.html', context)


@method_decorator(login_required,name='dispatch')    
class updateAddress(View):
    def get(self,request,pk):
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        addr = Customer.objects.get (pk=pk)
        form = CustomerProfileForm(instance=addr)
        context = {
            'form' : form,
            'totalitem' :totalitem,
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



@login_required
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


@login_required
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

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
        totalamount = amount + 40
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render (request, 'home/addtocart.html', locals())

# class checkout(View):
#     def get(self,request):
#         user = request.user 
#         addresses = Customer.objects.filter(user=user) 
#         cart_items = Cart.objects.filter(user=user)  
        
#         # Calculate total amount
#         total_amount = sum(item.quantity * item.product.discounted_price for item in cart_items) + 40
        
#         # Razorpay integration
#         razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#         razor_amount = int(total_amount * 100)
#         razor_data = {"amount": razor_amount, "currency": "INR", "receipt": "order_rcptid_12"}
#         payment_response = razorpay_client.order.create(data=razor_data) #prints the payment response
#         order_id = payment_response['id']
#         order_status = payment_response['status']
        
#         # Save payment information
#         if order_status == 'created':
#              payment = Payment(
#                  user=user,
#                  amount=total_amount,
#                  razorpay_order_id=order_id,
#                  razorpay_payment_status=order_status
#              )
#              payment.save()
        
#         context = {
           
#             'user': user,
#             'addresses': addresses,
#             'cart_items': cart_items,
#             'total_amount': total_amount,
#             'razoramount': razor_amount,
#             'order_id': order_id,
#         }
#         return render(request, 'home/checkout.html', context)


@method_decorator(login_required,name='dispatch')
class checkout(View):
     def get(self,request):
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        
        user = request.user
        addresses = Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)  
        total_amount = 0
        for item in cart_items:
            value = item.quantity * item.product.discounted_price
            total_amount += value
        total_amount += 40
        razoramount = int(total_amount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        {'id': 'order_OBWNt85ppmEius', 'entity': 'order', 'amount': 5500, 'amount_paid': 0, 'amount_due': 5500, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1715940266}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
             payment = Payment(
                 user=user,
                 amount=razoramount,
                 razorpay_order_id=order_id,
                 razorpay_payment_status = order_status
             )
             payment.save()
        context = {
            'user': user,
            'addresses': addresses,
            'cart_items': cart_items,
            'total_amount': total_amount,
            'razoramount' : razoramount,
            'order_id' : order_id,
            'totalitem' : totalitem,
        }
        return render(request, 'home/checkout.html',context)


@login_required
def payment_done(request):
    order_id=request.GET.get('order_id') 
    payment_id=request.GET.get('payment_id') 
    cust_id=request.GET.get('cust_id') 
    print("payment_done : oid = ",order_id," pid = ",payment_id," cid = ",cust_id)
    user=request.user 
    return redirect("orders")
    customer=Customer.objects.get(id=cust_id)
    #To update payment status and payment id
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    #To save order details
    cart=Cart.objects.filter(user=user) 
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")        
   
@login_required   
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user) 
    context ={
        'order_placed': order_placed,
        'totalitem' :totalitem
    }
    return render(request, 'home/orders.html' ,context)


@login_required
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

@login_required
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

@login_required
def search(request):
    query = request.GET.get('search')
    totalitem = 0
    product = None  # Initialize product variable
    if query:
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Products.objects.filter(title__icontains=query)
    context = {
        'totalitem': totalitem,
        'product': product,
    }  
    return render(request, 'home/search.html', context)


# Helper function to check if the user is a superuser
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()  # Initialize the form here for GET request

    return render(request, 'home/add_product.html', {'form': form})


@user_passes_test(is_superuser)
def update_product(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'home/update_product.html', {'form': form, 'product': product})

@user_passes_test(is_superuser)
def delete_product(request,pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'home/delete_product.html', {'product': product})


@user_passes_test(is_superuser)
def product_list(request):
    products = Products.objects.all()
    return render(request, 'home/product_list.html', {'products': products})    