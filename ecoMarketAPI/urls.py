from django.urls import path
from .views import OrderCreateAPIView, OrderListAPIView, ProductCategoryList, ProductList, delete_cookie, add_to_cart, get_cart, RegisterAPIView, LoginAPIView, ProductDetailView, ReviewView, ReviewDetailView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path("order-create/", OrderCreateAPIView.as_view()),
    path("order-list/", OrderListAPIView.as_view()),
    path("product-category-list/", ProductCategoryList.as_view()),
    path("product-list/", ProductList.as_view()),
    path("product-list/<int:pk>/add-to-cart", add_to_cart),
    path("product-list/<int:id>/add-review", ReviewView.as_view()),
    path("product-list/<int:id>/review/<int:review_id>", ReviewDetailView.as_view()),
    path("product-list/<int:id>", ProductDetailView.as_view()),
    path("cart/",get_cart),
    path("cart/delete/<int:product_id>", delete_cookie)
]
