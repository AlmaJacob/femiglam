from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.

def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    else:
        if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            data=authenticate(username=uname,password=password)
            if data:
                login(req,data)
                if data.is_superuser:
                    req.session['shop']=uname     #create
                    return redirect(shop_home)
                else:
                    req.session['user']=uname
                    return redirect(user_home)
            else:
                messages.warning(req, "Invalid Username or Password")
                return redirect(shop_login)
    return render(req,'login.html')

def shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(shop_login)

def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        password=req.POST['password']

        try:
            data=User.objects.create_user(first_name=uname,email=email,
                                        username=email,password=password)
            data.save()
        except:
            messages.warning(req, "Username or Email already exist")
            return redirect(register)
        return redirect(shop_login)
    else:
        return render(req,'register.html')
    
#-----------------ADMIN-------------------------------------------------
def shop_home(req):
       if 'shop' in req.session:
              Products=Product.objects.all()
              return render (req,'shop/shop_home.html',{'Product':Products})
       else:
              return redirect(shop_login)                                                                                                   


def add_product(req):
       if req.method=='POST':
              id=req.POST['pro_id']
              name=req.POST['name']
              price=req.POST['price']
              offer_price=req.POST['offer_price']
              file=req.FILES['img']
              data=Product.objects.create(pro_id=id,name=name,price=price,offer_price=offer_price,img=file)
              data.save()
       return render(req,'shop/add_product.html')

def edit_pro(req,id):
       pro=Product.objects.get(pk=id)
       if req.method=='POST':
              e_id=req.POST['pro_id']
              name=req.POST['name']
              price=req.POST['price']
              offer_price=req.POST['offer_price']
              file=req.FILES.get('img')
              print(file)
              if file:
                     Product.objects.filter(pk=id).update(pro_id=e_id,name=name,price=price,offer_price=offer_price,img=file)
              
              else:
                     Product.objects.filter(pk=id).update(pro_id=e_id,name=name,price=price,offer_price=offer_price)
                     
              return redirect(shop_home)
       return render(req,'shop/edit_product.html',{'data':pro})

def delete_pro(req,id):
       data=Product.objects.get(pk=id)
       url=data.img.url
       url=url.split('/')[-1]
       os.remove('media/'+url)
       data.delete()
       return redirect(shop_home) 

def bookings(req):
       bookings=Buy.objects.all()[::-1][:2]
       print(bookings)
       return render(req,'shop/bookings.html',{'data':bookings})

#------------------USER------------------------------------------------
def user_home(req):
    return render(req,'user/user_home.html')

def about(req):
    return render(req,'user/about.html')

def contact(req):
    return render(req,'user/contact.html')
def blog(req):
    return render(req,'user/blog.html')

def shop_home(req):
    return render(req,'shop/shop_home.html')

def add_pro(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            specifications=req.POST['specifications']
            price=req.POST['price']
            offer_price=req.POST['offer_price']
            brand=req.POST['brand']
            color=req.POST['color']
            highlights=req.POST['highlights']
            warranty=req.POST['warranty']
            services=req.POST['services']
            stock=req.POST['stock']
            img=req.FILES['img']
            product = Product(pid=pid,name=name,specifications=specifications,
                price=price,offer_price=offer_price,brand=brand,color=color,
                highlights=highlights,warranty=warranty,services=services,
                stock=stock,img=img
                )
            product.save()  
            return redirect(shop_home)
        else:
            return render(req,'shop/add_product.html')
    else:
        return redirect(shop_login)

def view_booking(req):
    return render(req,'shop/bookings.html')

def add_to_cart(req,pid):
          product=Product.objects.get(pk=pid)
          print(product)
          user=User.objects.get(username=req.session['user'])
          print(user)
          data=Cart.objects.create(user=user,product=product)
          data.save()
          return redirect(cart_display)

def cart_display(req):
        log_user=User.objects.get(username=req.session['user'])
        data=Cart.objects.filter(user=log_user)
        return render(req,'user/cart_display.html',{'data':data})

def delete_cart(req,id):
       data=Cart.objects.get(pk=id)
       data.delete()
       return redirect(cart_display)   

def buy_pro(req,id):
       product=Product.objects.get(pk=id) 
       user=User.objects.get(username=req.session['user'])
       price=product.offer_price
       data=Buy.objects.create(user=user,product=product,price=price)
       data.save()
       return redirect(user_home)
def user_view_booking(req):
       user=User.objects.get(username=req.session['user'])
       data=Buy.objects.filter(user=user)
       return render(req,'user/view_bookings.html',{'data':data})
def view_product(req,id):
       log_user=User.objects.get(username=req.session['user'])
       product=Product.objects.get(pk=id)
       try:
          Cart=Cart.objects.get(product=product,user=log_user)
       except:
              Cart=None       
       return render(req,'user/view_pro.html',{'product':product,'Cart':Cart})