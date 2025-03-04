from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
from django.db.models.fields import CharField


# Create your models here.

class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    descriptions=models.TextField()
    price=models.IntegerField()
    offer_price=models.IntegerField()
    brand=models.TextField()
    ingredients=models.TextField()
    expiry=models.TextField()
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
    qty=models.IntegerField(default=1)
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
class Contact(models.Model):
    name = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    
# from django.db import models

# class BlogPost(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(_("Payment Status"), default=PaymentStatus.PENDING,max_length=254, blank=False, null=False)
    provider_order_id = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    payment_id = models.CharField(_("Payment ID"), max_length=36, null=False, blank=False)
    signature_id = models.CharField(_('Signature ID'),max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"
    
    
class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    phn=models.IntegerField()
    house=models.TextField()
    street=models.TextField()
    pin=models.IntegerField()
    state=models.TextField()


class Details(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    offer_price = models.IntegerField()
    stock = models.IntegerField()
    weight = models.TextField()
