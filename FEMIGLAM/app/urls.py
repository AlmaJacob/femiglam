from django.urls import path
from . import views
from django.urls import path
from .views import buy_product
from .views import order_success


urlpatterns = [
    path('login',views.shop_login),
    path('logout',views.shop_logout),
    path('register',views.register),
    # ------------SHOP-------------
     path('shop',views.shop_home),
    path('add_pro',views.add_pro),
    path('delete_product/<pid>',views.delete_product),
    path('edit/<pid>',views.edit_product),
    path('view_booking',views.view_bookings),
    path('cancel_order/<pid>',views.cancel_order),




    # ------------USER-------------
    
    path('',views.user_home),
    path('profile',views.profile),
    path('update_username',views.update_username),
    path('about',views.about),
    path('blog',views.blog),
    path('contact',views.contact),
    path('view_pro/<id>',views.view_product),
    path('view_cart',views.view_cart),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('cart_disp',views.cart_display),
    path('delete_cart/<id>',views.delete_cart),
    # path('buy_pro/<id>',views.buy_pro),
    path('bookings',views.bookings),
    path('qty_in/<cid>',views.qty_in),
    path('qty_dec/<cid>',views.qty_dec),
    path('cart_pro_buy/<cid>',views.cart_pro_buy),
    # path('pro_buy/<pid>',views.pro_buy),
    path('clear_cart',views.clear_cart),
    path('checkout/<pid>',views.cart_display),
    path('shop_now',views.shop_now),
    path('buy_pro/<int:pk>/',views.buy_product),
    path('order_success', views.order_success),
    # path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('buy_now_checkout/<pid>', views.buy_now_checkout),
    path('cart_checkout', views.cart_checkout),
    path('order_payment', views.order_payment, name='order_payment'),
    path('callback',views.callback,name="callback"),
    path('order_payment2',views.order_payment2,name="order_payment2"),
    path('callback2',views.callback2,name="callback2"),
    path('address',views.address),
    path('delete_address/<pid>',views.delete_address),

]
