from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import authenticate
from ..serializers import UserSerializers
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password
import jwt
from ecommerce.settings import SECRET_KEY
from django.contrib.auth import logout


@api_view(["POST"])
def register(request):
    data=request.data
    data["password"]
    user=User.objects.create_user(**data)
    # serializer=UserSerializers(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response({"created":serializer.data},status=status.HTTP_201_CREATED)
    # return Response(serializer.errors)
    return Response({"created":"create successfully"},status=status.HTTP_201_CREATED)
    
@api_view(["POST"])
def login(request):
    try:
        my_data=request.data 
        user=User.objects.get(email=my_data["email"])
        token=jwt.encode({"id":user.id},key=SECRET_KEY, algorithm="HS256")
        my_user=authenticate(password=my_data["password"],username=user.username)
       
        print(user.email)
        if  my_user.id is  user.id :
            return Response({"login":"login successfully"},status=status.HTTP_200_OK)
    except Exception as ex : 
        return Response({"errors":"wrong password or email"},status=status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    inst=request.user
    print(inst)
    new_user=request.data
    new_user["password"]=make_password(new_user["password"])
    serializer=UserSerializers(data=new_user,instance=inst)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializers(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    user = User.objects.all()
    serializer = UserSerializers(user, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, id):
    try:
        user = User.objects.get(id=id).delete()
        return Response({"message" : "deleted successfully"} , status=status.HTTP_204_NO_CONTENT)
    except Exception as ex : 
        return Response ({"message" : "user Not Found"} ,status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, id):
    try:
        myUser=User.objects.filter(id=id)
        serializer=UserSerializers(myUser ,many=True)
        return Response(serializer.data)
    except Exception as ex : 
        return Response ({"message" : "user Not Found"} ,status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request,id):
    try:
        inst=User.objects.get(id=id)
        new_data=request.data
        new_data["password"]=make_password(new_data["password"])
        serializer=UserSerializers(data=new_data ,instance=inst)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    except Exception as ex : 
        return Response ({"message" : "user Not Found"} ,status=status.HTTP_404_NOT_FOUND)
    

    










