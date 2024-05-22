from django.test import TestCase
from django.contrib.auth.models import User
from .forms import (
    LoginForm, 
    CustomerRegistrationForm, 
    PasswordChangeForm, 
    PasswordResetForm, 
    SetPasswordForm, 
    CustomerProfileForm, 
    ProductForm
)
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Customer, Products


class FormsTestCaseLogInCustReg(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_form_with_invalid_data(self):
        # Providing invalid form data (missing password)
        form_data = {'username': 'testuser', 'password': ''}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="LoginForm should not be valid with missing password")

    def test_login_form_intentional_failure(self):
        # Providing valid form data
        form_data = {'username': 'testuser', 'password': 'password123'}
        form = LoginForm(data=form_data)
        # Intentional incorrect assertion to force test failure
        self.assertFalse(form.is_valid(), msg="Intentional failure: LoginForm should be valid with correct data")   


    def test_customer_registration_form_fields(self):
         # Providing invalid form fields.
        form = CustomerRegistrationForm()
        expected_fields = ['username','password1','email','password2']
        actual_fields = list(form.fields.keys())
        self.assertEqual(expected_fields,actual_fields,msg="CustomerRegistrationForm fields are not in the expected order or are missing")


    def test_customer_registration_form_invalid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'passkey'
        }

        form = CustomerRegistrationForm (data = form_data)
        self.assertTrue(form.is_valid(),msg="CustomerRegistrationForm should not be valid with non-matching passwords")


def test_customer_registration_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }

        form = CustomerRegistrationForm (data = form_data)
        self.assertTrue(form.is_valid(),msg="CustomerRegistrationForm should not be valid with non-matching passwords")


class PasswordResetFormTestCase(TestCase):
    def test_password_reset_form_valid_data(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com')
        form_data = {'email': 'testuser@example.com'}
        form = PasswordResetForm(data=form_data)
        self.assertTrue(form.is_valid(), msg="PasswordResetForm should be valid with correct data")

    

class SetPasswordFormTestCase(TestCase):
    def test_set_password_form_valid_data(self):
        user = User.objects.create_user(username='testuser')
        form_data = {
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        }
        form = SetPasswordForm(user=user, data=form_data)
        self.assertTrue(form.is_valid(), msg="SetPasswordForm should be valid with matching new passwords")

    def test_set_password_form_invalid_data(self):
        user = User.objects.create_user(username='testuser')
        form_data = {
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword'
        }
        form = SetPasswordForm(user=user, data=form_data)
        self.assertFalse(form.is_valid(), msg="SetPasswordForm should not be valid with non-matching new passwords")

class CustomerProfileFormTestCase(TestCase):
    def test_customer_profile_form_valid_data(self):
        user = User.objects.create_user(username='testuser')
        customer = Customer.objects.create(user=user, name='Test User')
        form_data = {
            'name': 'Test User',
            'locality': 'Test Locality',
            'city': 'Test City',
            'mobile': '1234567890',
            'state': 'Test State',
            'zipcode': '123456'
        }
        form = CustomerProfileForm(data=form_data, instance=customer)
        self.assertTrue(form.is_valid(), msg="CustomerProfileForm should be valid with correct data")

    def test_customer_profile_form_invalid_data(self):
        user = User.objects.create_user(username='testuser')
        customer = Customer.objects.create(user=user, name='Test User')
        form_data = {
            'name': '',
            'locality': 'Test Locality',
            'city': 'Test City',
            'mobile': '1234567890',
            'state': 'Test State',
            'zipcode': '123456'
        }
        form = CustomerProfileForm(data=form_data, instance=customer)
        self.assertFalse(form.is_valid(), msg="CustomerProfileForm should not be valid with missing name")




class ProductFormTestCase(TestCase):
    def test_product_form_valid_data(self):
        form_data = {
            'title': 'Test Product',
            'selling_price': '100.00',
            'discounted_price': '90.00',
            'description': 'Test Description',
            'category': 'Test Category',
            'product_image': ''  # Assuming product_image is optional for the sake of this test
        }
        form = ProductForm(data=form_data)
        if not form.is_valid():
            print("Form errors:", form.errors)
        self.assertTrue(form.is_valid(), msg="ProductForm should be valid with correct data")

    def test_product_form_invalid_data(self):
        form_data = {
            'title': '',
            'selling_price': '100.00',
            'discounted_price': '90.00',
            'description': 'Test Description',
            'category': 'Test Category',
            'product_image': ''  # Assuming product_image is optional for the sake of this test
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="ProductForm should not be valid with missing title")
