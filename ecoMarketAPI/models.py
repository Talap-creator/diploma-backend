from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class ProductCategory(models.Model):
    id = models.AutoField(editable=False, primary_key=True)
    name = models.CharField(max_length=50)
    image = models.URLField(null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.review}'
      
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.URLField(null=True)
    quantity = quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=5, max_digits=10)
    reviews = models.ManyToManyField(Review, default=None, blank=True)
    def __str__(self):
        return self.title


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    reference_point = models.CharField(max_length=255)
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.IntegerField(default=150, editable=False)
    items = models.ManyToManyField(OrderItem)
    total_amount = models.DecimalField(editable=False, max_digits=10, decimal_places=3, default=0)
    
    