from rest_framework import serializers
from .models import OrderItem, Order, Product, ProductCategory

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    order_number = serializers.IntegerField(read_only=True)
    total_amount = serializers.DecimalField(read_only=True, max_digits = 10, decimal_places = 3)
    created_at = serializers.DateTimeField(read_only=True)
    delivery_cost = serializers.IntegerField(read_only=True)
    ordered_products = serializers.CharField(read_only=True, max_length = 5000)
    class Meta:
        model = Order
        fields = "__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"