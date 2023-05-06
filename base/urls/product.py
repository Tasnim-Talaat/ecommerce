from django.urls import path
from ..views import products

urlpatterns = [
    path('all/', products.get_allproduct),
    path('product/<int:id>/', products.get_product),
    path('create/', products.create_product),
    path('delete/<int:id>/', products.delete_product),
    path('update/<int:id>/', products.update_product),
    path('rev/<int:id>/', products.createProductReview),
]