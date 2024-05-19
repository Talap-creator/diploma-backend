from rest_framework import serializers
from .models import OrderItem, Order, Product, ProductCategory, Review
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'write-only': True}
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password = validated_data['password']  ,first_name=validated_data['first_name'],  last_name=validated_data['last_name'])
        return user


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    reviews = ReviewSerializer(many=True, default=[])
    class Meta:
        model = Product
        fields = "__all__"
        
class OrderItemSerializer(serializers.ModelSerializer):
    product= ProductSerializer()
    class Meta:
        model = OrderItem
        fields = "__all__"
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, default=[])
    class Meta:
        model = Order
        fields = "__all__"
        