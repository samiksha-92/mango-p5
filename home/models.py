from django.db import models

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
