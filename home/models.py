from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY_CHOICES = (

    ('DR', 'Dress'),
    ('SH', 'Shirts'),
    ('ACC', 'Accessories'),

)

class Products (models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=3)
    product_image = models.ImageField(upload_to = 'product',blank=True,null=True)
    def __str__(self):
        return self.title
        


STATE_CHOICES = (
('Andaman & Nicobar Islands','Andaman & Nicobar Islands'), 
('Andhra Pradesh','Andhra Pradesh'),
('Arunachal Pradesh','Arunachal Pradesh'), 
('Assam','Assam'),
('Bihar','Bihar'), 
('Chandigarh','Chandigarh'), 
('Chattisgarh','Chattisgarh'),
('Dadra & Nagar Haveli','Dadra & Nagar Haveli'), 
('Daman and Diu','Daman and Diu'), 
('Delhi','Delhi'),
('Goa','Goa'),
('Gujrat','Gujrat'), 
('Haryana','Haryana'),
('Himachal Pradesh','Himachal Pradesh'), 
('Jammu & Kashmir','Jammu & Kashmir'), 
('Jharkhand','Jharkhand'), 
('Karnataka','Karnataka'), 
('Kerala','Kerala'), 
('Lakshadweep','Lakshadweep'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra'), 
('Manipur','Manipur'), 
('Meghalaya','Meghalaya'), 
('Mizoram','Mizoram'), 
('Nagaland','Nagaland'), 
('Odisa','Odisa'), 
('Puducherry','Puducherry'), 
('Punjab','Punjab'), 
('Rajasthan','Rajasthan'), 
('Sikkim','Sikkim'),
('Tamil Nadu','Tamil Nadu'), 
('Telangana','Telangana'), 
('Tripura','Tripura'), 
('Uttarakhand','Uttarakhand'), 
('Uttar Pradesh','Uttar Pradesh'), 
('West Bengal','West Bengal'),
)


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price   



class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price        