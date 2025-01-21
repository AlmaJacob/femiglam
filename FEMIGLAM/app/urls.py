from django.urls import path
from . import views


urlpatterns = [
    path('',views.shop_login),
    path('logout',views.shop_logout),
    path('register',views.register),

    # ------------SHOP-------------
     path('shop',views.shop_home),
    path('logout',views.shop_logout),
    path('add_pro',views.add_pro),
    path('delete_product/<pid>',views.delete_product),
    path('edit/<pid>',views.edit_product),
    path('view_booking',views.view_bookings),
    path('cancel_order/<pid>',views.cancel_order),




    # ------------USER-------------
    
    path('user_home',views.user_home),
    path('about',views.about),
    path('blog',views.blog),
    path('contact',views.contact),
    path('view_pro/<id>',views.view_product),
    path('view_cart',views.view_cart),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('cart_disp',views.cart_display),
    path('delete_cart/<id>',views.delete_cart),
    path('buy_pro/<id>',views.buy_pro),
    path('bookings',views.bookings),
    path('qty_in/<cid>',views.qty_in),
    path('qty_dec/<cid>',views.qty_dec),
    path('cart_pro_buy/<cid>',views.cart_pro_buy),
    path('pro_buy/<pid>',views.pro_buy),
    path('checkout/<pid>',views.cart_display),

]
