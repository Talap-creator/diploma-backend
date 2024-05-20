from django.shortcuts import render
from decimal import Decimal
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.utils import timezone
from .models import OrderItem, Order, Product, ProductCategory, Review
from .serializers import OrderSerializer, ProductSerializer, ProductCategorySerializer, RegistrationSerializer, UserSerializer, ReviewSerializer
import json
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


def get_cart(request):
    # Retrieve the cart from the session
    cart = request.session.get('cart', {})

    # Convert the cart dictionary into a list of product details
    cart_items = []
    total_price = 0
    for product_id, product in cart.items():
        product_model = Product.objects.get(pk=product_id)
        total_price += product_model.price * product['quantity']
        cart_items.append({
            'id': product_id,
            'quantity': product['quantity'],
            'price': product_model.price,
            'title': product_model.title
        })
    response_data = {
        'cart': cart_items,
        'total_price': total_price
    }
    return JsonResponse(response_data)

# Check -----------------------------------------
def delete_cookie(request, *args, **kwargs):
    product_id = kwargs.get('product_id')
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        return JsonResponse({'success': 'Product removed from cart', 'cart': cart})
    return JsonResponse({'error': 'Product not found in cart'}, status=400)

@require_http_methods(["POST"])  
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_id = str(pk)
    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'quantity': 1, 'price': str(product.price)}

    # Save the cart back to the session
    request.session['cart'] = cart

    # Return success response
    return JsonResponse({'success': 'Product added to cart', 'cart': cart})

# EDIT

User = get_user_model()

class OrderCreateAPIView(APIView):
    serializer_class = OrderSerializer
    def post(self, request):
        data = request.data
        user = request.user
        order_items = request.session.get('cart', {})
        order = Order.objects.create(
            user=user,
            phone_number=data['phone_number'],
            address=data['address'],
            reference_point=data['reference_point'],
            comments=data['comments'],
            total_amount=0
        )
        for product_id, items in order_items.items():
            product = Product.objects.get(pk=product_id)
            order_item = OrderItem.objects.create(
            product=product,
            quantity=items['quantity']
            )
            if product.quantity < items['quantity']:
                return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
            product.quantity -= items['quantity']
            order.items.add(order_item)
            order.total_amount += product.price * items['quantity']
        request.session['cart'] = {}
        order.save()
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
    