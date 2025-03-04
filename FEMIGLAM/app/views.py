from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import AddressForm
from django.core.mail import send_mail

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Cart, Buy
from django.urls import reverse
# from .models import BlogPost
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import razorpay
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def shop_login(req):
    if 'shop' in req.session:
        # req.session.flush()
        return redirect(shop_home)
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
                messages.warning(req,'invalid username or password')
                return redirect(shop_login)
    return render(req,'login.html')

def shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(shop_login)

def register(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        
        try:
            validate_password(password)
            
            
            if User.objects.filter(email=email).exists():
                messages.warning(req, 'User with this email already exists.')
                return redirect(register)

            
            user = User.objects.create_user(first_name=name, username=email, email=email, password=password)
            user.save()

            
            send_mail(
                'Account Registration',
                'Your Cargo account registration was successful.',
                settings.EMAIL_HOST_USER,
                [email]
            )

            messages.success(req, 'Registration successful. Please log in.')
            return redirect(shop_login)

        except ValidationError as e:
            messages.error(req, ', '.join(e)) 
            return redirect(register)
        
    return render(req, 'register.html')



    
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

def profile(req):
 return render(req,'user/profile.html')

def update_username(request):
    if request.method == "POST":
        new_first_name = request.POST.get("name")
        new_username = request.POST.get("username")

        
        if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            messages.error(request, "This username is already taken. Please choose another one.")
            return redirect(profile) 

        
        if new_first_name and new_username:
            request.user.first_name = new_first_name
            request.user.username = new_username
            request.user.save()
            messages.success(request, "Username updated successfully!")
        else:
            messages.error(request, "Username and Name cannot be empty.")

    return redirect(profile)

def about(req):
    return render(req,'user/about.html')

def shop_now(req):
    data=Product.objects.all()
    return render(req,'user/shop_now.html',{'product':data})
def contact(req):
    if req.method == "POST":
        name = req.POST["name"]
        email = req.POST["email"]
        message = req.POST["message"]

        send_mail(
            subject=f"New Contact Form Submission from {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=email,
            recipient_list=["femifemiglam@gmail.com"], 
            fail_silently=True,
        )

        messages.success(req, "Your message has been sent successfully!")
        return redirect(contact )  
    return render(req,'user/contact.html',)

def blog(req):
    return render(req,'user/blog.html')

def view_booking(req):
    return render(req,'shop/bookings.html')

#giving address when buynow is clicked

def buy_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # Save address data or process order
            address = form.cleaned_data['address']
            # You can save it to the database or process further
            return redirect(order_success)  # Redirect to success page after saving

    else:
        form = AddressForm()

    return render(request, 'user/buy_product.html', {'form': form, 'product': product})


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
    try:
        data=Cart.objects.get(pk=cid)
        if data.product.stock > data.qty:
            data.qty+=1
            data.save()
        else:
            messages.warning(req, "Cannot increase quantity. Stock unavailable.")
    except Cart.DoesNotExist:
        messages.error(req, "Cart item not found.")
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

# def pro_buy(req,pid):
#     product=Product.objects.get(pk=pid)
#     user=User.objects.get(username=req.session['user'])
#     qty=1
#     price=product.offer_price
#     buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
#     buy.save()
#     return redirect(view_bookings)



def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart_display.html',{'cart':data})
    

def cart_display(req):
        log_user=User.objects.get(username=req.session['user'])
        data=Cart.objects.filter(user=log_user)
        return render(req,'user/cart_display.html',{'data':data})

def delete_cart(req, id):
    data = Cart.objects.get(pk=id)
    data.delete()
    return redirect(cart_display)


# def buy_pro(req, id):
#     cart = Cart.objects.get(pk=id)
#     user = User.objects.get(username=req.session['user'])
#     price = cart.offer_price
#     qty = 1
#     data = Buy.objects.create(user=user, cart=cart, qty=qty, price=price)
#     data.save()
#     return render(req,'user/buy_product.html')

def buy_pro(req, id):
    try:
        cart = Cart.objects.get(pk=id)  # Fetch cart by id
    except Cart.DoesNotExist:
        return HttpResponse("Cart item does not exist.", status=404)  # Handle error

    user = User.objects.get(username=req.session['user'])  # Fetch user
    price = cart.product.offer_price
    qty = 1
    data = Buy.objects.create(user=user,qty=qty,price=price)
    data.save()

    return render(req, 'user/buy_product.html')
def bookings(req):
    buy = Buy.objects.all()[::-1]
    return render(req, 'user/bookings.html', {'buy': buy})


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

def order_success(request):
    return render(request,'user/order_succes.html')

# def blog_detail(request, post_id):
#     post = get_object_or_404(BlogPost, id=post_id)
#     return render(request, 'blog_detail.html', {'post': post})


# ---------------------------------payment------------------------ 

def order_payment(request):
    if 'user' in request.session and 'selected_product' in request.session:
        user = User.objects.get(username=request.session['user'])
        name = user.first_name
        product_data = request.session['selected_product']
        
       
        product_id = product_data['product_id']
        product_name = product_data['product_name']
        amount = product_data['price']
        selected_weight = product_data['weight']
        address_id = product_data['address_id']
        payment_method = product_data['payment_method']
        
       
        address = Address.objects.get(id=address_id)

        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id = razorpay_order['id']
        
        
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()

    
        print(f"Order Created: {order_id}, Amount: {amount}")

       
        return render(
            request,
            "user/payment.html",  
            {
                "callback_url": "http://127.0.0.1:8000/razorpay/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return render(request, 'user/login.html') 



@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()

        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
        else:
            order.status = PaymentStatus.FAILURE
            order.save()

       
        if 'selected_product' in request.session:
            del request.session['selected_product']

        return render(request, "callback.html", context={"status": order.status})


def order_payment2(request):
    if 'user' in request.session and 'total_amount' in request.session:
        user = User.objects.get(username=request.session['user'])
        name = user.first_name
        total_amount = request.session['total_amount']
        address_id = request.session['address_id']

        # Fetch address
        address = Address.objects.get(id=address_id)

        # Create Razorpay order
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(total_amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id = razorpay_order['id']

        # Create Order object
        order = Order.objects.create(
            name=name, amount=total_amount, provider_order_id=order_id
        )
        order.save()

        print(f"Order Created: {order_id}, Amount: {total_amount}")

        # Render payment page
        return render(
            request,
            "user/payment.html",  
            {
                "callback_url": "http://127.0.0.1:8000/razorpay/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return redirect(shop_login)


@csrf_exempt
def callback2(request):

    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status})  
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status}) 

    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status}) 


# ---------------------------------payment------------------
def buy_now_checkout(req, pid):
    if 'user' in req.session:
        product_instance = Product.objects.filter(pk=pid).first()
        current_url = req.build_absolute_uri()

        if not product_instance:
            return redirect('product_not_found')

        details = Details.objects.filter(product=product_instance)
        selected_weight = req.GET.get('weight')

        if selected_weight:
            selected_detail = details.filter(weight=selected_weight).first()   
        else:
            selected_detail = details.first()

        if not selected_detail:
            return render(req, 'user/view_details.html', {
                'message': 'No details available for this product with the selected weight.'})

        user = User.objects.get(username=req.session['user'])
        existing_addresses = Address.objects.filter(user=user)

        if req.method == 'POST':
            address_id = req.POST.get('address') 
            payment_method = req.POST.get('payment_method')

            
            if address_id:
                address = Address.objects.get(id=address_id)
            else:
                name = req.POST.get('name')
                phn = req.POST.get('phn')
                house = req.POST.get('house')
                street = req.POST.get('street')
                pin = req.POST.get('pin')
                state = req.POST.get('state')

                address = Address.objects.create(
                    user=user, name=name, phn=phn, house=house, 
                    street=street, pin=pin, state=state
                )

        
            req.session['selected_product'] = {
                'product_id': product_instance.id,
                'product_name': product_instance.name,
                'price': selected_detail.offer_price,
                'weight': selected_weight,
                'address_id': address.id,
                'payment_method': payment_method
            }

            quantity = 1
            if selected_detail.stock > 0:
                selected_detail.stock -= quantity
                selected_detail.save()  

                price = selected_detail.offer_price
                buy = Buy.objects.create(
                    details=selected_detail, user=user, quantity=quantity, 
                    t_price=price, address=address
                )
                buy.save()

                if payment_method == "online":
                    return redirect('order_payment')  
                else:
                    return redirect(bookings) 

            else:
                return render(req, 'user/view_details.html', {
                    'message': 'Sorry, this product is out of stock.'})

        return render(req, 'user/checkout.html', {
            'product': product_instance,
            'details': selected_detail,
            'addresses': existing_addresses,
            'current_url': current_url,
        })
    else:
        return redirect(shop_login)




def cart_checkout(req):
    current_url = req.build_absolute_uri()
    if 'user' not in req.session:
        return redirect('cosmetic_login')

    user = User.objects.get(username=req.session['user'])
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return render(req, 'user/cart.html', {'message': 'Your cart is empty.'})

  
    total_amount = sum(cart.qty * cart.details.offer_price for cart in cart_items)
    
    existing_addresses = Address.objects.filter(user=user)

    if req.method == 'POST':
        address_id = req.POST.get('address')
        payment_method = req.POST.get('payment_method')

        # Create or select an address
        if address_id:
            address = Address.objects.get(id=address_id)
        else:
            address = Address.objects.create(
                user=user,
                name=req.POST.get('name'),
                phn=req.POST.get('phn'),
                house=req.POST.get('house'),
                street=req.POST.get('street'),
                pin=req.POST.get('pin'),
                state=req.POST.get('state')
            )

   
        if payment_method == "online":
            
            req.session['total_amount'] = total_amount
            req.session['address_id'] = address.id

            return redirect('order_payment')  

        else:
           
            for cart in cart_items:
                selected_detail = cart.details
                quantity = cart.quantity

                if selected_detail.stock >= quantity:
                  
                    Buy.objects.create(
                        details=selected_detail,
                        user=user,
                        quantity=quantity,
                        t_price=selected_detail.offer_price * quantity,
                        address=address
                    )

                   
                    selected_detail.stock -= quantity
                    selected_detail.save()

                  
                    cart.delete()
                else:
                    return render(req, 'user/cart.html', {
                        'message': f'Insufficient stock for {cart.details.product.name}.'
                    })

            return redirect(bookings) 

    return render(req, 'user/cart_checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'addresses': existing_addresses,
        'current_url': current_url,
    })



def address(req):
    return_url = req.GET.get('returnUrl') 
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        data = Address.objects.filter(user=user)
        
        if req.method == 'POST':
          
            name = req.POST['name']
            phn = req.POST['phn']
            house = req.POST['house']
            street = req.POST['street']
            pin = req.POST['pin']
            state = req.POST['state']
            
            
            Address.objects.create(user=user, name=name, phn=phn, house=house, street=street, pin=pin, state=state)
            
          
            if return_url:
                return redirect(return_url)
            else:
               
                return redirect(shop_home)  
        
        return render(req, "user/addaddress.html", {'data': data, 'return_url': return_url})
    else:
        return redirect(shop_login)  




def delete_address(req, pid):
    return_url = req.GET.get('returnUrl')  
    print(return_url)
    if 'user' in req.session:
        
        address = Address.objects.get(pk=pid)
        address.delete()
        
       
        if return_url:
            return redirect(return_url)
        else:
          
            return redirect(user_home) 
    else:
        return redirect(shop_login)



