from django.urls import path
from . import views


urlpatterns = [
    path('',views.shop_login),
    path('register',views.register),

    # ------------shop-------------
    path('shop',views.shop_home),
    path('logout',views.shop_logout),
    path('add_pro',views.add_pro),
    path('view_booking',views.view_booking),




    # ------------USER-------------
    
    path('user_home',views.user_home),
    path('about',views.about),
    path('blog',views.blog),
    path('contact',views.contact),
    path('view_pro/<id>',views.view_product),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('cart_disp',views.cart_display),
    path('delete_cart/<id>',views.delete_cart),
    path('buy_pro/<id>',views.buy_pro),
    path('view_bookings',views.user_view_booking),

]