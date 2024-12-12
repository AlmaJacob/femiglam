from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.conf import settings

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
        pswd=req.POST['pswd']

        try:
            data=User.objects.create_user(first_name=uname,email=email,
                                        username=email,password=pswd)
            data.save()
        except:
            messages.warning(req, "Username or Email already exist")
            return redirect(register)
        return redirect(shop_login)
    else:
        return render(req,'register.html')



def user_home(req):
    return render(req,'user/user_home.html')


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
