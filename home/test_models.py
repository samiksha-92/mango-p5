from django.test import TestCase
from django.contrib.auth.models import User
from .models import Products, Customer, Cart, Payment, OrderPlaced

class ModelsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.product = Products.objects.create(
            title='Test Product',
            selling_price=100.00,
            discounted_price=80.00,
            description='Test Description',
            category='DR',
        )
        self.customer = Customer.objects.create(
            user=self.user,
            name='Test Customer',
            locality='Test Locality',
            city='Test City',
            mobile=1234567890,
            zipcode=123456,
            state='Test State'
        )
        self.cart = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
        self.payment = Payment.objects.create(
            user=self.user,
            amount=200.00
        )
        self.order = OrderPlaced.objects.create(
            user=self.user,
            customer=self.customer,
            product=self.product,
            quantity=1,
            status='Pending',
            payment=self.payment
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_customer_str(self):
        self.assertEqual(str(self.customer), 'Test Customer')

    def test_cart_total_cost(self):
        self.assertEqual(self.cart.total_cost, 160.00)

    def test_order_total_cost(self):
        self.assertEqual(self.order.total_cost, 80.00)
