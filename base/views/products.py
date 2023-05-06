from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from ..serializers import ProductSerializers,ReviewSerializers
from ..models import Product,Review
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import status



# Create your views here.
@api_view(['GET'])
def get_allproduct(request):
    try:
        all_product=Product.objects.all()
        serializer=ProductSerializers(all_product,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as ex : 
        return Response (serializer.errors,status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):
    new_product=request.data
    serializer=ProductSerializers(data=new_product)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_product(request,id):
    inst=Product.objects.get(id=id)
    new_product=request.data
    serializer=ProductSerializers(data=new_product,instance=inst)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request,id):
    try:
        product=Product.objects.get(id=id).delete()
        return Response({'delete':"product deleted successfully"},status=status.HTTP_202_ACCEPTED)
    except Product.DoesNotExist:
        return Response({'delete':"product DoesNotExist"},status=status.HTTP_404_NOT_FOUNDD)
    except Exception as ex:
        return Response ({"message" : str(ex)} ,status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_product(request,id):
    try:
        product=Product.objects.filter(id=id)
        serializer=ProductSerializers(product,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as ex : 
        return Response (serializer.errors,status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request,id):
    myUser=request.user
    # print(request.user.id)
    myData=request.data
    myData["product"]=id
    myData["user"]=myUser.id
    # print(myData)
    serializer=ReviewSerializers(data=myData)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


    
    
