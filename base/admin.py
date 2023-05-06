from django.contrib import admin
from .models import Product , Order,OrderItem,ShippingAddress,Review
# Register your models here.
# admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category','user']
    list_editable = ['price']
    ordering = ['name','-price']
    list_filter = ['category', 'price']
    search_fields = ['name__startswith']