from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product (models.Model) : 
    name = models.CharField(max_length=200 , null=False , blank=False , default="Product")
    image = models.ImageField(null=True , blank=True)
    brand = models.CharField(max_length=200 , null=False , blank=False) 
    category = models.CharField(max_length=100 , null= False , blank=False,default="Other" )
    description = models.TextField() 
    rating = models.FloatField(null=False , default=0) 
    num_reviews = models.IntegerField(default=0)
    price = models.FloatField(null=False , blank=False) 
    count_in_stock = models.IntegerField(default=0 , null=False ,blank=False)
    created_at = models.DateTimeField(auto_now_add=True )
    user = models.ForeignKey(User , on_delete=models.CASCADE,null=True)
    def __str__(self) :
        return self.name
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(rating__lte=5), name='rating must be less than 5'),
            models.CheckConstraint(check=models.Q(price__gte=0), name='price must be less than 0'),
        ]
        db_table = 'Product'

class Review (models.Model) : 
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.FloatField(null=False) 
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        # constraints = [
        #     models.CheckConstraint(check=models.Q(rating__lte=5), name='rating must be less than 5'),
        # ]
        db_table = 'Review'
    # def __str__(self) :
    #     return self.rating

class Order(models.Model):
    payment_method = models.CharField(max_length=200)
    tax_price = models.FloatField(null=False , blank=False) 
    shipping_price = models.FloatField(null=False , blank=False) 
    total_price = models.FloatField(null=False , blank=False) 
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'Order'

class OrderItem(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(null=False , blank=False) 
    image = models.ImageField(null=True , blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,related_name="orderItem")
    class Meta:
        # constraints = [
        #     models.CheckConstraint(check=models.Q(quantity__lte=0), name='quantity must be less than 0'),
        #     # models.CheckConstraint(check=models.Q(price__lte=0), name='price must be less than 0'),
        # ]
        db_table = 'OrderItem'
    

class ShippingAddress(models.Model):
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    order = models.OneToOneField(Order, on_delete=models.CASCADE,related_name="shippingAddress")
    class Meta:
        db_table = 'ShippingAddress'
