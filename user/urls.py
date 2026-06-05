from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
        path('register',views.register,name='register'),
        path('user',views.userhome,name='userhome'),
        path('login',views.login_user,name="login"),
        path('logout',views.logout_user,name='logout'),
        path('details/<int:id>',views.productdetails,name='details'),
        path('profileview',views.profileview,name='profileview'),
        path('profileedit',views.editprofile,name='profileedit'),
        path('wishlist/<int:id>',views.addwishlist,name='wishlist'),
        path('wishview',views.viewwishlist,name="wishview"),
        path('wishremove/<int:id>',views.removewish,name='wishremove'),
        path('addcart/<int:id>',views.cartadd,name='addcart'),
        path('cartview',views.viewcart,name='cartview'),
        path('removecart/<int:id>',views.cartremove,name='removecart'),
        path('addqnty/<int:id>',views.cartqntyadd,name='addqnty'),
        path('subqnty/<int:id>',views.cartqntysub,name='subqnty'),
        path('pay',views.pay,name='pay'),
        path('feed/<int:id>',views.feedback,name="feedback"),
        path('cod',views.cod,name='cod'),
        path('orders',views.ordersview,name="orders"),
        path('orderdetails/<int:id>',views.orderdetails,name='orderdetails'),
        path('cancelorder/<int:id>',views.cancelorder,name='cancelorder'),
        path('upi',views.upi,name='upi'),
        path('payment_success',views.payment_success,name='payment_success'),  
        path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
        path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
        path('viewall',views.vall,name='viewall')
]
