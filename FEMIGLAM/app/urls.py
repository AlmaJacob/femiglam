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
]