from django.shortcuts import render
from decimal import Decimal
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.utils import timezone
from .models import OrderItem, Order, Product, ProductCategory
from .serializers import OrderSerializer, ProductSerializer, ProductCategorySerializer, RegistrationSerializer, UserSerializer
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

class LoginAPIView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))

        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            response.data = data
            response.status_code = status.HTTP_200_OK

        return response

class Cart(APIView):
    def get(self, request):
        cart = request.COOKIES.get('cart', {})
        return Response(cart)

class DeleteCookiesView(APIView):
    def get(self, request):
        cookie_name = 'cart'
        response = Response('Cookies deleted')
        response.delete_cookie('cart')
        return response

class CartAPIView(APIView):
    def post(self, request, pk):
        try:
            product_id = int(pk)
        except ValueError:
            return Response({'error': 'Invalid product ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Replace this with your logic for checking if the product exists
        # Assuming Product is a Django model
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Default to an empty dictionary if 'cart' is not present
        cart = request.COOKIES.get('cart', '{}')
        cart = json.loads(cart)
        cart_item_quantity = cart.get(str(product_id), 0)
        cart[str(product_id)] = cart_item_quantity + 1

        response_data = {'success': 'Product added to cart'}
        response = Response(response_data)
        # Convert the dictionary back to JSON
        response.set_cookie('cart', json.dumps(cart))
        return response

# EDIT

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_data = serializer.validated_data
        ordered_products = self.request.COOKIES.get('cart', {})
        ordered_products = json.loads(ordered_products)
        total_amount = Decimal('0.0')

        # Create Order instance
        order = Order.objects.create(
            address=order_data['address'],
            phone_number=order_data['phone_number'],
            reference_point=order_data['reference_point'],
        )

        print(f"Order created with order_number: {order.order_number}")

        for product_id, quantity in ordered_products.items():
            try:
                product = Product.objects.get(pk=int(product_id))
            except Product.DoesNotExist:
                return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            order_item = OrderItem.objects.create(
                product=product,
                quantity=quantity,
                order=order
            )
            order.add_to_ordered_products(product_id, quantity)
            total_amount += Decimal(quantity) * product.price
        # Update total_amount for the order
        order.total_amount = total_amount
        order.save(update_fields=['total_amount'])  # Explicitly update total_amount

        print(f"Order total_amount updated to: {order.total_amount}")
        serializer = OrderSerializer(order)
        headers = self.get_success_headers(serializer.data)
        response = Response({"data": serializer.data, "total_amount": total_amount}, status=status.HTTP_201_CREATED, headers=headers)
        response.delete_cookie('cart')
        return response

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        category_name = self.request.query_params.get('category_name', None)
        product_name = self.request.query_params.get('product_name', None)
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCategoryList(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
