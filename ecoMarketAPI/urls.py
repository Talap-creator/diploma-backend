from django.urls import path
from .views import OrderCreateAPIView, OrderListAPIView, ProductCategoryList, ProductList, Cart, CartAPIView, DeleteCookiesView, RegisterAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path("order-create/", OrderCreateAPIView.as_view()),
    path("order-list/", OrderListAPIView.as_view()),
    path("product-category-list/", ProductCategoryList.as_view()),
    path("product-list/", ProductList.as_view()),
    path("product-list/<int:pk>/add-to-cart/", CartAPIView.as_view()),
    path("cart/", Cart.as_view()),
    path("cart/delete", DeleteCookiesView.as_view())
]
