from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.utils import timezone
from .models import OrderItem, Order, Product, ProductCategory
from .serializers import OrderItemSerializer, OrderSerializer, ProductSerializer, ProductCategorySerializer
import json
from rest_framework.views import APIView
from rest_framework.response import Response


class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the current cart data from the request's cookies
        cart_data = request.COOKIES.get('cart_data', '{}')
        cart_data = json.loads(cart_data)

        # Process the request data and add the item to the cart
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)

        if item_id:
            cart_data[item_id] = cart_data.get(item_id, 0) + int(quantity)

        # Set the updated cart data in the response's cookies
        response = Response({'message': 'Item added to the cart'})
        response.set_cookie('cart_data', json.dumps(
            cart_data), max_age=3600)  # Set the max_age as needed

        return response

    def get(self, request):
        cart_data = request.COOKIES.get('cart_data', '{}')
        cart_data = json.loads(cart_data)
        return Response(cart_data)


class OrderitemList(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def post(self, request):
        product_list = request.COOKIES.get('cart_data', '{}')
        product_list = json.loads(product_list)
        order_data = {
            'phone_number': request.data.get('phone_number'),
            'order_items': product_list,
            'address': request.data.get('phone_number'),
            'reference_point': request.data.get('reference_point'),
            'comments': request.data.get('comments'),
            'total_amount': request.data.get('total_amount'),
        }

        # Use the serializer to create the order
        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderitemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


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


class ProductCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
