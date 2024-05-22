
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cart, Products
from .forms import CustomerRegistrationForm, CustomerProfileForm


# Create your tests here.


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Products.objects.create(
            title='Test Product',
            selling_price=120.0, 
            discounted_price=100.0,
            category='TestCategory'
        )
        self.cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=1)

    def test_index_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertEqual(response.context['totalitem'], 1)
        
    def test_index_view_unauthenticated(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertEqual(response.context['totalitem'], 0)

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/about.html')

    # def test_category_view(self):
    #     self.client.login(username='testuser', password='password')
    #     response = self.client.get(reverse('category', args=[self.product.category]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'home/category.html')
    #     self.assertEqual(response.context['totalitem'], 1)
    #     self.assertEqual(response.context['category'], self.product.category)

    def test_product_detail_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('product-detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/productdetail.html')
        self.assertEqual(response.context['totalitem'], 1)
        self.assertEqual(response.context['product'], self.product)

    # def test_customer_registration_view_get(self):
    #     response = self.client.get(reverse('customer_registration'), follow=True)
    # self.assertEqual(response.status_code, 200)

    def test_profile_view_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/profile.html')
        self.assertIsInstance(response.context['form'], CustomerProfileForm)

    def test_address_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('address'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/address.html')
        self.assertEqual(response.context['totalitem'], 1)
        self.assertEqual(list(response.context['address']), [])

    def test_add_to_cart_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('add-to-cart'), {'prod_id': self.product.id})
        self.assertEqual(response.status_code, 302)  # Should redirect after adding to cart

    

    def test_orders_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/orders.html')
        self.assertEqual(response.context['totalitem'], 1)
        self.assertEqual(list(response.context['order_placed']), [])
