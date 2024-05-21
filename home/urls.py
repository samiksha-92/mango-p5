"""mangomore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, PasswordResetForm, PasswordChangeForm,SetPasswordForm


urlpatterns = [
    path('',views.index,name = 'home'),
    path('about/', views.about,name="about"),
    path('category-title/<category>/', views.CategoryTitle.as_view(), name='category-title'),
    path('category/<slug:category>/',views.CategoryView.as_view(),name ='category'),
    path('product-detail/<int:pk>/',views.ProductDetail.as_view(),name = 'product-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
    #Storeowner website admin panel 
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/update/<int:pk>/', views.update_product, name='update_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    #login authentication
    path('customer-registration/', views.CustomerRegistrationView.as_view(), name='customer-registration'),
    #login 
    path('login/', auth_view.LoginView.as_view(template_name='home/login.html', authentication_form=LoginForm) , name='login'),
    path('success/', views.success_page, name='success-page'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login') , name='logout'),
    path('search/',views.search, name = 'search'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('pluscart/', views.plus_cart,name = 'plus_cart'),
    path('minuscart/', views.minus_cart,name = 'minus_cart'), 
    path('removecart/', views.remove_cart,name = 'remove_cart'),
    #password reset
    path('passwordreset/done/', auth_view.PasswordResetDoneView.as_view(template_name='home/passwordresetdone.html') , name='password_reset_done'),
    path('passwordresetconfirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='home/passwordresetconfirm.html',form_class=SetPasswordForm) , name='password_reset_confirm'),
    path('passwordresetcomplete/', auth_view.PasswordResetCompleteView.as_view(template_name='home/passwordresetcomplete.html') , name='password_reset_complete'),
    path('passwordreset/', auth_view.PasswordResetView.as_view(template_name='home/passwordreset.html', form_class=PasswordResetForm) , name='password_reset'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='home/changepassword.html', form_class=PasswordChangeForm, success_url='/passwordchangecomplete') , name='passwordchange'),
    path('passwordchangecomplete/', auth_view.PasswordChangeDoneView.as_view(template_name='home/passwordchangecomplete.html') , name='passwordchangecomplete'),
   

]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

admin.site.site_header = "MangoMore Administration"
admin.site.site_title = "MangoMore"
admin.site.site_index_title = "Welcome to MangoMore Thriftstore"



