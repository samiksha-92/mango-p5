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
    product_image = models.ImageField(upload_to = 'product')
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
    products = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.products.discounted_price   #products not product 