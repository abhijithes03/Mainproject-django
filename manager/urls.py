from django.contrib import admin
from django.urls import path
from manager import views

urlpatterns = [
    path('',views.home,name="home"),
    path('mgrhome',views.managerhome,name="mgrhome"),
    path('catgry',views.catgry,name='catgry'),
    path('perfume',views.perfumes,name='perfume'),
    path('viewperfume',views.viewperfume,name='viewperfume'),
    path('delete/<int:id>',views.deleteperfume,name="delete"),
    path('edit/<int:id>',views.editperfume,name='edit'),
    path('viewreg',views.viewregister,name='viewr'),
    path('rate',views.rate,name='rate'),
    path('vorders',views.vieworders,name='vorders'),
    path('vodetails/<int:id>',views.adminorderdetails,name="vodetails"),
    path('updateorder/<int:id>',views.orderupdate,name="updateorder"),
    path('cancel/<int:id>',views.Canceladmin,name='cancel'),
    path('complete/<int:id>',views.Completeadmin,name='complete'),
    
    
    
   
    

]
