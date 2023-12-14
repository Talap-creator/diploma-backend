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


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.URLField(null=True)
    quantity = quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=5, max_digits=10)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    reference_point = models.CharField(max_length=255)
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.IntegerField(default=150, editable=False)
    ordered_product_list = models.JSONField(editable=False, default=list)
    total_amount = models.DecimalField(editable=False, max_digits=10, decimal_places=3, default=0)
    def add_to_ordered_products(self, product_id, quantity):
        current_ordered_products = self.ordered_product_list

        # Append a new dictionary to the list
        current_ordered_products.append({"product_id": product_id, "quantity": quantity})

        # Update the ordered_product_list field and save the model instance
        self.ordered_product_list = current_ordered_products
        self.save(update_fields=['ordered_product_list'])
        
    def __str__(self):
        return str(self.total_amount)


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
