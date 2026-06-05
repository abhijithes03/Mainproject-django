from django.db import models
from django.contrib.auth.models import User
from manager.models import perfume,rating

# Create your models here.
class Register(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE) #Uses ForeignKey / OneToOne relation
    gender=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    postalcode=models.CharField(max_length=50)
    phonenumber=models.CharField(max_length=100)
    profilephoto=models.FileField(upload_to='media')
    

class wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(perfume,on_delete=models.CASCADE)
    

# 


class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(perfume,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.IntegerField()
    
class review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(perfume,on_delete=models.CASCADE)
    description=models.CharField(max_length=500)
    rate=models.ForeignKey(rating,on_delete=models.CASCADE)
 
 
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    totalamount=models.IntegerField()
    paymentmethod=models.CharField(max_length=50)
    paymentstatus=models.CharField(max_length=50,default='pending')
    orderstatus=models.CharField(max_length=50,default='pending')
    Carrier=models.CharField(max_length=100,null=True,blank=True)
    trackingid=models.CharField(max_length=100,null=True,blank=True)
    orderdate=models.CharField(max_length=50)
    deliverydate=models.CharField(max_length=50,null=True,blank=True)



class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(perfume,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.IntegerField()
    