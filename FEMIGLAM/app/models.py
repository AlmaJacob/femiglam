from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    descriptions=models.TextField()
    price=models.IntegerField()
    offer_price=models.IntegerField()
    brand=models.TextField()
    ingredients=models.TextField()
    warranty=models.TextField()
    stock=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    img=models.FileField()
    
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()

class Buy(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
