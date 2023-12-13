from django.urls import path
from .views import OrderitemList, OrderitemDetailView, OrderList, ProductCategoryList, ProductList, AddToCartView

urlpatterns = [
    path("", OrderitemList.as_view()),
    path("order-item/<int:pk>", OrderitemDetailView.as_view()),
    path("order-create/", OrderList.as_view()),
    path("order-list/", OrderList.as_view()),
    path("product-category-list/", ProductCategoryList.as_view()),
    path("product-list/", ProductList.as_view()),
    path("add-cookie/", AddToCartView.as_view()),
]
