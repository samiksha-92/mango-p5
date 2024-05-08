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
from .forms import LoginForm, MyPasswordResetForm

urlpatterns = [
    path('',views.index,name = 'home'),
    path('about/', views.about,name="about"),
    path('category-title/<category>/', views.CategoryTitle.as_view(), name='category-title'),
    path('category/<slug:category>/',views.CategoryView.as_view(),name ='category'),
    path('product-detail/<int:pk>/',views.ProductDetail.as_view(),name = 'product-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    #login authentication
    path('customer-registration/', views.CustomerRegistrationView.as_view(), name='customer-registration'),
    #login 
    path('accounts/login/', auth_view.LoginView.as_view(template_name='home/login.html', authentication_form=LoginForm) , name='login'),
    path('success/', views.success_page, name='success-page'),
    #password reset
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='home/password_reset.html', form_class=MyPasswordResetForm) , name='password_reset'),

]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)



