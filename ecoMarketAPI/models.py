from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

class OrderItem(models.Model):
    product = models.IntegerField()
    quantity = models.IntegerField(validators=[
           MinValueValidator(limit_value=0, message="Value must be greater than or equal to 0."),
        ])
    
class Order(models.Model):
    order_number = models.IntegerField(editable=False)
    products = models.ManyToManyField(OrderItem)
    phone_number = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    address = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    reference_point = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    comments = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    total_amount = models.DecimalField(editable=False, decimal_places=5, max_digits=10)
    created_at = models.DateTimeField()
    delivery_cost = models.IntegerField(editable=False, default=150)
    ordered_products = models.TextField(editable=False)
    
class ProductCategory(models.Model):
    id = models.IntegerField(editable=False, primary_key=True)
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)])
    image = models.URLField(null=True, editable=False)
    
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    description = models.TextField()
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    image = models.URLField(null=True, editable=False)
    quantity = quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=5, max_digits=10)