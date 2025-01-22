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
        data=Product.objects.all()
        print (data)
        return render(req,'shop/shop_home.html',{'product':data})
    else:
        return redirect(shop_login)

def add_pro(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            descriptions=req.POST['descriptions']
            price=req.POST['price']
            offer_price=req.POST['offer_price']
            brand=req.POST['brand']
            ingredients=req.POST['ingredients']
            expiry=req.POST['expiry']
            stock=req.POST['stock']
            img=req.FILES['img']
            product = Product(pid=pid,name=name,descriptions=descriptions,
                price=price,offer_price=offer_price,brand=brand,ingredients=ingredients,expiry=expiry,
                stock=stock,img=img)
            product.save()  
            return redirect(shop_home)
        else:
            return render(req,'shop/add_product.html')
    else:
        return redirect(shop_login)
    
            
def edit_product(req,pid):
    if req.method=='POST':
        # pid=req.POST['pid']
        name=req.POST['name']
        descriptions=req.POST['descriptions']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        brand=req.POST['brand']
        ingredients=req.POST['ingredients']
        expiry=req.POST['expiry']
        stock=req.POST['stock']
        img=req.FILES.get('img')
        if img:
            Product.objects.filter(pk=pid).update(pid=pid,name=name,descriptions=descriptions,
                price=price,offer_price=offer_price,brand=brand,ingredients=ingredients,expiry=expiry,stock=stock)
            data=Product.objects.get(pk=pid)
            data.img=img
            data.save()
        else:
            Product.objects.filter(pk=pid).update(pid=pid,name=name,descriptions=descriptions,
                price=price,offer_price=offer_price,brand=brand,ingredients=ingredients,expiry=expiry,stock=stock)
        return redirect(shop_home)
    else:
        data=Product.objects.get(pk=pid)
        return render(req,'shop/edit.html',{'data':data})

def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)


def view_bookings(req):
    buy=Buy.objects.all()[::-1]
    return render(req,'shop/view_bookings.html',{'buy':buy})

def cancel_order(req,pid):
    data =Buy.objects.get(pk=pid)
    data.delete()
    return redirect(view_bookings) 

#------------------USER------------------------------------------------
def user_home(req):
    data=Product.objects.all()
    return render(req,'user/user_home.html',{'product':data})

def about(req):
    return render(req,'user/about.html')

def shop_now(req):
    data=Product.objects.all()
    return render(req,'user/shop_now.html',{'product':data})

def contact(req):
    return render(req,'user/contact.html')
def blog(req):
    return render(req,'user/blog.html')

def view_booking(req):
    return render(req,'shop/bookings.html')

def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,product=product)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return redirect(view_cart)

def qty_in(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.price= data.qty*data.product.offer_price
    data.save()
    return redirect(view_cart)

def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    print(data.qty)
    if data.qty==0:
        data.delete()
    return redirect(view_cart)


def cart_pro_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    user=cart.user
    qty=cart.qty
    price=product.offer_price*qty
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(view_bookings)

def pro_buy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.offer_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(view_bookings)



def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart_display.html',{'cart':data})
    

def cart_display(req):
        log_user=User.objects.get(username=req.session['user'])
        data=Cart.objects.filter(user=log_user)
        return render(req,'user/cart_display.html',{'data':data})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Cart, Buy
from django.contrib.auth.models import User
import os


# Create your views here.

def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    else:
        if req.method == 'POST':
            uname = req.POST['uname']
            password = req.POST['password']
            data = authenticate(username=uname, password=password)
            if data:
                login(req, data)
                if data.is_superuser:
                    req.session['shop'] = uname  # create
                    return redirect(shop_home)
                else:
                    req.session['user'] = uname
                    return redirect(user_home)
            else:
                messages.warning(req, "Invalid Username or Password")
                return redirect(shop_login)
    return render(req, 'login.html')


def shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(shop_login)


def register(req):
    if req.method == 'POST':
        uname = req.POST['uname']
        email = req.POST['email']
        password = req.POST['password']

        try:
            data = User.objects.create_user(first_name=uname, email=email, username=email, password=password)
            data.save()
        except:
            messages.warning(req, "Username or Email already exist")
            return redirect(register)
        return redirect(shop_login)
    else:
        return render(req, 'register.html')


# -----------------ADMIN-------------------------------------------------

def shop_home(req):
    if 'shop' in req.session:
        data = Product.objects.all()
        return render(req, 'shop/shop_home.html', {'product': data})
    else:
        return redirect(shop_login)


def add_pro(req):
    if 'shop' in req.session:
        if req.method == 'POST':
            pid = req.POST['pid']
            name = req.POST['name']
            descriptions = req.POST['descriptions']
            price = req.POST['price']
            offer_price = req.POST['offer_price']
            brand = req.POST['brand']
            ingredients = req.POST['ingredients']
            expiry = req.POST['expiry']
            stock = req.POST['stock']
            img = req.FILES['img']
            product = Product(pid=pid, name=name, descriptions=descriptions,
                              price=price, offer_price=offer_price, brand=brand, ingredients=ingredients, expiry=expiry,
                              stock=stock, img=img)
            product.save()
            return redirect(shop_home)
        else:
            return render(req, 'shop/add_product.html')
    else:
        return redirect(shop_login)


def edit_product(req, pid):
    if req.method == 'POST':
        name = req.POST['name']
        descriptions = req.POST['descriptions']
        price = req.POST['price']
        offer_price = req.POST['offer_price']
        brand = req.POST['brand']
        ingredients = req.POST['ingredients']
        expiry = req.POST['expiry']
        stock = req.POST['stock']
        img = req.FILES.get('img')
        if img:
            Product.objects.filter(pk=pid).update(pid=pid, name=name, descriptions=descriptions,
                                                  price=price, offer_price=offer_price, brand=brand, ingredients=ingredients, expiry=expiry, stock=stock)
            data = Product.objects.get(pk=pid)
            data.img = img
            data.save()
        else:
            Product.objects.filter(pk=pid).update(pid=pid, name=name, descriptions=descriptions,
                                                  price=price, offer_price=offer_price, brand=brand, ingredients=ingredients, expiry=expiry, stock=stock)
        return redirect(shop_home)
    else:
        data = Product.objects.get(pk=pid)
        return render(req, 'shop/edit.html', {'data': data})


def delete_product(req, pid):
    data = Product.objects.get(pk=pid)
    file = data.img.url
    file = file.split('/')[-1]
    os.remove('media/' + file)
    data.delete()
    return redirect(shop_home)


def view_bookings(req):
    buy = Buy.objects.all()[::-1]
    return render(req, 'shop/view_bookings.html', {'buy': buy})


def cancel_order(req, pid):
    data = Buy.objects.get(pk=pid)
    data.delete()
    return redirect(view_bookings)


# ------------------USER------------------------------------------------

def user_home(req):
    data = Product.objects.all()
    return render(req, 'user/user_home.html', {'product': data})


def about(req):
    return render(req, 'user/about.html')


def contact(req):
    return render(req, 'user/contact.html')


def blog(req):
    return render(req, 'user/blog.html')


def bookings(req):
    buy = Buy.objects.all()[::-1]
    return render(req, 'user/bookings.html', {'buy': buy})


def add_to_cart(req, pid):
    product = Product.objects.get(pk=pid)
    user = User.objects.get(username=req.session['user'])
    try:
        cart = Cart.objects.get(user=user, product=product)
        cart.qty += 1
        cart.save()
    except:
        data = Cart.objects.create(product=product, user=user, qty=1)
        data.save()
    return redirect(view_cart)


def qty_in(req, cid):
    data = Cart.objects.get(pk=cid)
    data.qty += 1
    data.price = data.qty * data.product.offer_price
    data.save()
    return redirect(view_cart)


def qty_dec(req, cid):
    data = Cart.objects.get(pk=cid)
    data.qty -= 1
    data.save()
    if data.qty == 0:
        data.delete()
    return redirect(view_cart)


# def cart_pro_buy(req, cid):
#     cart = Cart.objects.get(pk=cid)
#     product = cart.product
#     user = cart.user
#     qty = cart.qty
#     price = product.offer_price * qty
#     buy = Buy.objects.create(product=product, user=user, qty=qty, price=price)
#     buy.save()
#     return redirect(view_bookings)


def pro_buy(req, pid):
    product = Product.objects.get(pk=pid)
    user = User.objects.get(username=req.session['user'])
    qty = 1
    price = product.offer_price
    buy = Buy.objects.create(product=product, user=user, qty=qty, price=price)
    buy.save()
    return redirect(view_bookings)


def view_cart(req):
    user = User.objects.get(username=req.session['user'])
    data = Cart.objects.filter(user=user)
    total_price = sum(item.product.offer_price * item.qty for item in data)  # Calculate total price
    return render(req, 'user/cart_display.html', {'cart': data, 'total_price': total_price})


def cart_display(req):
    log_user = User.objects.get(username=req.session['user'])
    data = Cart.objects.filter(user=log_user)
    total_price = sum(item.product.offer_price * item.qty for item in data)  # Calculate total price
    return render(req, 'user/cart_display.html', {'data': data, 'total_price': total_price})


def delete_cart(req, id):
    data = Cart.objects.get(pk=id)
    data.delete()
    return redirect(cart_display)


def buy_pro(req, id):
    product = Product.objects.get(pk=id)
    user = User.objects.get(username=req.session['user'])
    price = product.offer_price
    qty = 1
    data = Buy.objects.create(user=user, product=product, qty=qty, price=price)
    data.save()
    return redirect(view_bookings)


def user_view_booking(req):
    user = User.objects.get(username=req.session['user'])
    data = Buy.objects.filter(user=user)
    return render(req, 'user/view_bookings.html', {'data': data})

def delete_cart(req,id):
       data=Cart.objects.get(pk=id)
       data.delete()
       return redirect(cart_display)   

def buy_pro(req,id):
    product=Product.objects.get(pk=id) 
    user=User.objects.get(username=req.session['user'])
    price=product.offer_price
    qty=1
    data=Buy.objects.create(user=user,product=product,qty=qty,price=price)
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


def clear_cart(req):
    data=Cart.objects.all()
    data.delete()
    return redirect(view_cart)