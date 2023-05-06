from django.urls import path
from ..views import order


urlpatterns = [
    path('all/', order.getAllOrders),
    path('add/', order.addOrderItems),
    path('order/<int:id>/', order.getOrderById),
    path('myorder/', order.getMyOrders),
    path('paid/<int:id>/', order.updateOrderToPaid),
    path('deliver/<int:id>/', order.updateOrderToDelivered),
    
]