from django.contrib import admin
from .models import OrderItem, Order, Product, ProductCategory, Review

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Review)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
admin.site.register(ProductCategory, ProductAdmin)


# Register your models here.
