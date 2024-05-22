from django.urls import path
from .views import OrderCreateAPIView, OrderListAPIView, ProductCategoryList, ProductList, RegisterAPIView, LoginAPIView, ProductDetailView, ReviewView, ReviewDetailView, get_csrf, ProductByCategoryViewSet, ReviewListView, CartItemAddView, CartDetailView, CartItemUpdateView, CartItemDeleteView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path("order-create/", OrderCreateAPIView.as_view()),
    path("order-list/", OrderListAPIView.as_view()),
    path("product-category-list/", ProductCategoryList.as_view()),
    path("product-list/", ProductList.as_view()),
    path("product-list/<int:pk>/add-to-cart", CartItemAddView.as_view()),
    path("cart/delete/<int:product_id>",  CartItemDeleteView.as_view()),
    path("product-list/<int:id>/review-list", ReviewListView.as_view()),
    path("product-list/<int:id>/add-review", ReviewView.as_view()),
    path("product-list/<int:id>/review/<int:review_id>", ReviewDetailView.as_view()),
    path("product-list/<int:id>", ProductDetailView.as_view()),
    path("product-by-category/<int:category_id>", ProductByCategoryViewSet.as_view({'get': 'list'})),
    path("csrf/", get_csrf),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
]
