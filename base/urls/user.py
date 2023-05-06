from django.urls import path
from ..views import user

urlpatterns = [
    path('register/', user.register),
    path('login/', user.login),
    path('update/', user.updateUserProfile),
    path('user/', user.getUserProfile),
    path('alluser/', user.getUsers),
    path('delete/<int:id>/', user.deleteUser),
    path('userId/<int:id>/', user.getUserById),
    path('updateuser/<str:id>/', user.updateUser),
    
]