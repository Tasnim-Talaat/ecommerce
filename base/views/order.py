from django.shortcuts import render,HttpResponse
from ..models import Order
from rest_framework.decorators import api_view,permission_classes
from ..serializers import OrderSerializers
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import status
from django.utils import timezone

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAllOrders(request):
    # all_order=Order.objects.all()
    # serializer=OrderSerializers(data=all_order,many=True)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    # return Response({"message":serializer.errors} , status=status.HTTP_400_BAD_REQUEST)
    try:
        order=Order.objects.all()
        serializer=OrderSerializers(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as ex : 
        return Response (serializer.errors,status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request,id):
    try:
        order=Order.objects.filter(id=id)
        serializer=OrderSerializers(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except : 
        return Response({"message":serializer.errors} , status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated]) 
def getMyOrders(request) : 
    try : 
        my_user = request.user
        orders = Order.objects.filter(user_id=my_user.id)
        serializer = OrderSerializers(orders , many=True)
        return Response({"message":serializer.data},status=status.HTTP_200_OK)
    except : 
        return Response({"message":serializer.errors} , status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    new_order=request.data
    serializer=OrderSerializers(data=new_order)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request,id):
    try:
        order=Order.objects.get(id=id)
        if not order.is_paid  :
            order.is_paid=True
            order.paid_at=timezone.now()
            order.save()
            return Response({"message":order},status=status.HTTP_200_OK)
    except Exception as ex : 
        return Response ({"message" : "user Not Found"} ,status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request,id):
    try:
        order=Order.objects.get(id=id)
        if not order.is_delivered  :
            order.is_delivered=True
            order.delivered_at=timezone.now()
            order.save()
            return Response({"message":order},status=status.HTTP_200_OK)
    except Exception as ex : 
        return Response ({"message" : "user Not Found"} ,status=status.HTTP_404_NOT_FOUND)




