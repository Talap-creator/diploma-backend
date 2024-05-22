from django.shortcuts import render
from decimal import Decimal
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.utils import timezone
from .models import OrderItem, Order, Product, ProductCategory, Review, Cart, CartItem
from .serializers import OrderSerializer, ProductSerializer, ProductCategorySerializer, RegistrationSerializer, UserSerializer, ReviewSerializer, CartItemSerializer, CartSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from django.middleware.csrf import get_token


def get_csrf(request):
    csrf_token = get_token(request)
    response = JsonResponse({'csrfToken': csrf_token})
    return response


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

from django.views.decorators.csrf import csrf_protect

class CartItemAddView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        print("USER",request.user)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
        if not created:
            cart_item.quantity += 1  # Assuming you want to increment the quantity if the item already exists
        cart_item.save()
        cart.items.add(cart_item)
        return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_201_CREATED)

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return Cart.objects.get(user=self.request.user)

class CartItemUpdateView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CartItemDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, product_id):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(product_id=product_id, cart=cart)
            cart_item.delete()
            return Response({'message': 'Item removed from cart successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

User = get_user_model()

class OrderCreateAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user

        # Fetch user's cart from the database
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Create a new order
        order = Order.objects.create(
            user=user,
            phone_number=data['phone_number'],
            address=data['address'],
            reference_point=data['reference_point'],
            comments=data['comments'],
            total_amount=0  # Initially set to zero and will update as items are added
        )

        # Process each item in the cart
        for cart_item in cart.items.all():
            product = cart_item.product
            quantity = cart_item.quantity

            # Check if sufficient stock is available
            if product.quantity < quantity:
                return Response({'error': 'Not enough stock for {}'.format(product.name)}, status=status.HTTP_400_BAD_REQUEST)

            # Create order item
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

            # Update product stock and order total
            product.quantity -= quantity
            product.save()
            order.total_amount += product.price * quantity
            order.items.add(order_item)

        # Clear the cart once the order is placed
        cart.items.clear()
        order.save()

        # Return the serialized order
        return Response(OrderSerializer(order).data)
    
class OrderListAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        print(type(OrderSerializer(orders, many=True).data))
        return Response(OrderSerializer(orders, many=True).data)


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class ProductCategoryList(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        product_id = self.kwargs.get('id')
        review_id = self.kwargs.get('review_id')
        obj = queryset.filter(pk=review_id).first()
        if not obj:
            raise NotFound("No Review found for the provided Product ID and Review ID")
        return obj

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    
class ReviewView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    def perform_create(self, serializer):
        user = User.objects.get(username=self.request.user)
        serializer.save(user=user)
    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.get(username=self.request.user)
        product = Product.objects.get(pk=kwargs['id'])
        review = Review.objects.create(
            user=user,
            rating=data['rating'],
            review=data['review'],
            product=product
        )
        return Response(ReviewSerializer(review).data)
    
    
class ProductByCategoryViewSet(viewsets.ViewSet):
    serializer_class = ProductSerializer
    def list(self, request, category_id):
        products = Product.objects.filter(category_id=category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    