from rest_framework import serializers
from .models import Product,Order,OrderItem,ShippingAddress,Review
from django.contrib.auth.models import User
from django.db.models import Sum


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model =User
        fields ="__all__"

class ReviewSerializers(serializers.ModelSerializer):
    def validate_rating(self,value):
        if value < 1 or value > 5:
            print("value",value)
            raise serializers.ValidationError("rate must be between 1 to 5")
        else:
            # print("value",value)
            return value
    class Meta:
        model =Review
        fields = "__all__"
        # ["name","rating","comment"]
        
   

class ProductSerializers(serializers.ModelSerializer):
    reviews=serializers.SerializerMethodField()
    num_reviews=serializers.SerializerMethodField()
    rating=serializers.SerializerMethodField()
    class Meta:
        model =Product
        fields ="__all__"
        
    def get_reviews(self,obj):
        all_reviews=Review.objects.filter(product=obj)
        serializer=ReviewSerializers(all_reviews,many=True)
        return serializer.data
    
    def get_num_reviews(self,obj):
        len_reviews=len(Review.objects.filter(product=obj))
        return len_reviews
    
    def get_rating(self,obj):
        len_reviews=len(Review.objects.filter(product=obj))
        reviews = Review.objects.filter(product=obj).aggregate(rate=(Sum('rating'))/len_reviews)
        # print(reviews)
        # rate=reviews.rating__sum/int(len_reviews)
        return reviews
        
class OrderSerializers(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    orderItem=serializers.SerializerMethodField()
    shippingAddress=serializers.SerializerMethodField()
    class Meta:
        model =Order
        fields ="__all__"

    def get_user(self,obj):
        my_user=User.objects.filter(order=obj)
        serializer=UserSerializers(my_user,many=True)
        return serializer.data



    def get_orderItem(self,obj):
        all_orderItem=OrderItem.objects.filter(order=obj)
        serializer=OrderItemSerializers(all_orderItem,many=True)
        return serializer.data
    
    def get_shippingAddress(self,obj):
        all_shippingAddress=ShippingAddress.objects.filter(order=obj)
        serializer=ShippingAddressSerializers(all_shippingAddress,many=True)
        return serializer.data


class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model =OrderItem
        fields ="__all__"

class ShippingAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model =ShippingAddress
        fields ="__all__"
