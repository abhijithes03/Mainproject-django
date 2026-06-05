from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Group
from django.contrib import messages
from .models import*
from django.contrib.auth import authenticate,login,logout,get_user_model
from manager.models import perfume,category
from datetime import date
from django.conf import settings
import stripe 
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse

# Create your views here.
stripe.api_key=settings.STRIPE_SECRET_KEY
def register(request):
    if request.method == "POST":
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        username=request.POST['uname']
        password=request.POST['pwrd']
        email=request.POST['email']
        gender=request.POST.get('gender')
        address=request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        phone=request.POST['phone']
        postal=request.POST['poscode']
        pimage=request.FILES.get('pimage')
        
        if not all([first_name,last_name,username,password,email,gender,address,city,state,phone,postal,pimage]):
            messages.error(request,'All Fields are required')
            return redirect('register')
        else:
            
        
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email)
            user.save()
            customer=Register.objects.create(user=user,gender=gender,address=address,city=city,state=state,postalcode=postal,phonenumber=phone,profilephoto=pimage)
            customer_obj,create=Group.objects.get_or_create(name='CUSTOMER')
            customer_obj.user_set.add(user)
            customer_obj.save()
            messages.success(request,'Registration successful!')
            return redirect('home')
        
    return render(request,'common/register.html')


        
def login_user(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='CUSTOMER').exists():
            return redirect('userhome')
        else:
            return redirect('mgrhome')
    if request.method == 'POST':
        username=request.POST['uname']
        password=request.POST['pwrd']
        u=authenticate(request,username=username,password=password)
        if u is not None:       #here u is same as the user in register, the u contains the user details.
            if u.groups.filter(name='CUSTOMER').exists():
                login(request,u)
                return redirect('userhome')
            else:
                login(request,u)
                return redirect('mgrhome')
        else:
            messages.error(request,'User credintials are not correct')
            return redirect('login')
    return render(request,'user/login.html')
  


def logout_user(request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('home')
    
    
def userhome(request):
    if request.user.is_authenticated:
        search=request.GET.get('search')
        categorys=request.GET.get('category')
        c=category.objects.all()
        t=perfume.objects.all()
        if search:
            t=t.filter(perfumename__icontains=search)
        if categorys:
            t=t.filter(perfume_category_id=categorys)
        wishlist_item=wishlist.objects.filter(user=request.user).values_list('item_id',flat=True)
        # [(1,)(2,)][(1),(2)],that filtering is getting the item IDs of a particular user’s wishlist.
        return render(request,'user/userhome.html',{'data':t,'w':wishlist_item,'c':c})
    else:
        return redirect('login')


def productdetails(request,id):
    
    ed=get_object_or_404(perfume,id=id)
    s=rating.objects.all()
    rv=review.objects.filter(item_id=id)
    cart_item=cart.objects.filter(item_id=ed.id,user=request.user).first()

    return render(request,'user/perfumedetails.html',{'data':ed,'cart':cart_item,'data2':s,'data3':rv})
    
def profileview(request):
    s=get_object_or_404(Register,user=request.user)  #here user in model have all details about user table data|Uses ForeignKey / OneToOne relation
    
    return render(request,'user/profile.html',{'i':s})

def editprofile(request):
    ed=get_object_or_404(Register,user=request.user) ##here also we can use id ,but if id use give id in path,related html(editprofile and profile).
    if request.method=='POST':
        ed.user.first_name=request.POST.get('fname')
        ed.user.last_name=request.POST.get('lname')
        ed.user.email=request.POST.get('email')
        ed.address=request.POST.get('address')
        ed.gender=request.POST.get('gender')
        ed.city=request.POST.get('city')
        ed.state=request.POST.get('state')
        ed.postalcode=request.POST.get('poscode')
        ed.phonenumber=request.POST.get('phone')
        if 'pphoto' in request.FILES:
            ed.profilephoto=request.FILES['pphoto']
        ed.user.save()
        ed.save()
        messages.success(request,'Profile Edited Successfully')
        return redirect('profileview')
    return render(request,'user/editprofile.html',{'data':ed})

def addwishlist(request,id):
    s=perfume.objects.get(id=id)
    wishlist_item=wishlist.objects.filter(
        user=request.user,
        item=s
        
    ).first()  #checking if logged user have item in wishlist table,
               #(Is there any row in the wishlist table where this user = current logged-in user AND this item = selected perfume?) 
    
    if wishlist_item:
        wishlist_item.delete()
    else:
        wishlist.objects.create(user=request.user,item=s)    
    return redirect('userhome')

def viewwishlist(request):
    
    u=request.user
    s=wishlist.objects.filter(user=u)
    return render(request,'user/wishview.html',{'data':s})
        
def removewish(request,id):
    wishlist.objects.filter(id=id,user=request.user).delete()
    messages.success(request,'Item removed from wishlist')
    return redirect('wishview')

def cartadd(request,id):
    if request.method=='POST':
        quantity=request.POST.get('quantity')
        if not quantity:
            messages.error(request,'Please Enter Quantity')
            return redirect('details',id=id)
        try:
            qnty = int(quantity)
        except ValueError:
            messages.error(request, 'Invalid Quantity')
            return redirect('details', id=id)

        s=get_object_or_404(perfume,id=id)
        price=s.perfume_price
        stock=s.perfume_stock
        u=request.user
        qnty=int(quantity)
        
        if qnty > stock:
                
                messages.error(request,"Out of stock")
                return redirect('userhome')
        elif qnty < 1:
                
                messages.error(request,"Invalid quantity")
                return redirect('userhome')
        else:
            
                h=cart.objects.create(quantity=quantity,price=price,item_id=s.id,user=u)
                h.save()
                messages.success(request,"Added to cart successfully")
                return redirect('userhome')
        
        
def viewcart(request):
        u=request.user
        s=cart.objects.filter(user=u)
        
        grandtotal=0
        for i in s:
            i.total_price=i.quantity*i.price
            grandtotal=grandtotal+i.total_price
            
        return render(request,'user/cartview.html',{'data':s,'data2':grandtotal})
    
def cartremove(request,id):
    cart.objects.filter(item_id=id,user=request.user).delete()
    messages.success(request,'Item removed from your cart')
    return redirect('cartview')

def cartqntyadd(request,id):
    t=get_object_or_404(perfume,id=id)
   
    stock=t.perfume_stock
    
    c=get_object_or_404(cart,item_id=id,user=request.user)
    qnty=c.quantity
    
    if qnty<stock:
        c.quantity=qnty+1
        c.save()
        return  redirect('cartview')
    
        
def cartqntysub(request,id):
    t=get_object_or_404(perfume,id=id)
    c=get_object_or_404(cart,item_id=id,user=request.user)
    qnty=c.quantity
    cid=c.item_id
    if qnty>1:
        c.quantity=qnty-1
        c.save()
        return redirect('cartview')
    elif qnty==1 :
        return redirect('removecart',id=cid)
    
    
def pay(request):
    
    s=cart.objects.filter(user=request.user)
    grandtotal=0
    for i in s:
        i.total_price=i.quantity * i.price
        grandtotal=grandtotal+i.total_price
    return render(request,'user/pay.html',{'data':s,'grandtotal':grandtotal})

def feedback(request,id):
    t=get_object_or_404(perfume,id=id)
    u=request.user
    if request.method=='POST':
        rate=request.POST.get('rate')
        feedback=request.POST.get('feed')
        s=review.objects.create(description=feedback,rate_id=rate,user=u,item_id=t.id)
        s.save()
        messages.success(request,'Thank You For Your Feedback')
        return redirect('details',id=t.id)


def cod(request):
    if request.method=='POST':
        paymentmthd='Cash On Delivery'
        u=request.user
        s=cart.objects.filter(user=u)
        grandtotal=0
        for i in s:
            
            i.total_price=i.quantity * i.price
            grandtotal=grandtotal+i.total_price
            
           
        dat=date.today()
        h=Order.objects.create(user=u,totalamount=grandtotal,paymentmethod=paymentmthd,
                              paymentstatus='pending',orderstatus='pending',orderdate=dat )
        h.save()
        
        order=h
        for k in s:
            qnty=k.quantity     #qnty,price, and productid is for storing it in orderitem table
            price=k.price
            product=k.item
            
            j=OrderItem.objects.create(quantity=qnty,price=price,order_id=order.id,product_id=product.id)
            j.save()
            cart.objects.filter(item_id=product.id,user=request.user).delete()
            t=get_object_or_404(perfume,id=product.id)
            m=0
            m=t.perfume_stock-qnty
            perfume.objects.filter(id=product.id).update(perfume_stock=m)
        messages.success(request,'Purchase Successfull')
        return render(request,'user/orderpage.html',{'data':grandtotal})
       
def ordersview(request):
    s=Order.objects.filter(user=request.user).order_by('-id')
    return render(request,'user/myorders.html',{'data':s})

def orderdetails(request,id):
    t=get_object_or_404(Order,id=id)
    g=OrderItem.objects.filter(order_id=id)
    return render(request,'user/orderdetails.html',{'data':t,'data1':g})

def cancelorder(request,id):
    if request.method=='POST':
        t=get_object_or_404(Order,id=id,user=request.user)
        
        
        if t.paymentmethod!='UPI':
        
            Order.objects.filter(id=id).update(orderstatus='Cancelled')
            s=OrderItem.objects.filter(order_id=id)
            for i in s:
                q=i.quantity
                pt=i.product.id
                ed=get_object_or_404(perfume,id=pt)
                stock=0
                ps=ed.perfume_stock
                stock=ps+q
                perfume.objects.filter(id=i.product_id).update(perfume_stock=stock)    
                   
            messages.success(request,'Order Cancelled')
            return redirect('orders')
        else:
            Order.objects.filter(id=id,paymentstatus='paid').update(orderstatus='Cancelled')
            y=OrderItem.objects.filter(order_id=id)
            for i in y:
                qt=i.quantity
                pti=i.product.id
                de=get_object_or_404(perfume,id=pti)
                stck=0
                pss=de.perfume_stock
                stck=pss+qt
                perfume.objects.filter(id=i.product_id).update(perfume_stock=stck)    
                   
            messages.success(request,'Order Cancelled:Refund will be processed shortly')
            return redirect('orders')
    
def upi(request):
    
    cart_items=cart.objects.filter(user=request.user)
    line_items = []

    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.item.perfumename,
                },
                'unit_amount': int(item.item.perfume_price * 100),
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://127.0.0.1:8000/payment_success',   
        cancel_url='http://127.0.0.1:8000/cartview',
    )

    return redirect(session.url)    
    

def  payment_success(request):
    
        paymentmthd='UPI'
        u=request.user
        s=cart.objects.filter(user=u)
        gtotal=0
        for i in s:
            totalprice=i.quantity*i.price
            gtotal=gtotal+totalprice
        dat=date.today()
        h=Order.objects.create(user=u,paymentmethod=paymentmthd,totalamount=gtotal,orderdate=dat,paymentstatus='paid',
                               orderstatus='pending')
        h.save()
        
        order=h
        for k in s:
            qnty=k.quantity
            price=k.price
            product=k.item
            
            j=OrderItem.objects.create(quantity=qnty,price=price,order_id=order.id,product_id=product.id)
            j.save()
            cart.objects.filter(item_id=product.id,user=request.user).delete()
            t=get_object_or_404(perfume,id=product.id)
            m=0
            m=t.perfume_stock-qnty
            perfume.objects.filter(id=product.id).update(perfume_stock=m)
        messages.success(request,'Purchase Successfull')
        return render(request,'user/orderpageupi.html',{'data':gtotal})
    
    
    
def generate_token():
     return get_random_string(20)

def password_reset_request(request):
    if request.method == "POST":
         email = request.POST.get('email')
         try:
             user = User.objects.get(email=email)
         except User.DoesNotExist:
             messages.error(request, "User with this email does not exist.")
             return redirect('password_reset_request')

         token =default_token_generator.make_token(user)
         uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
         reset_url = request.build_absolute_uri(reverse('password_reset_confirm',kwargs={'uidb64':uidb64,'token':token}))
         subject = "Password Reset Request"
         message = render_to_string('common/password_reset_email.html', {
             'user': user,
             'reset_url': reset_url,
         })
         send_mail(subject, message,settings.DEFAULT_FROM_EMAIL, [user.email])
         messages.success(request, "A password reset link has been sent to your email.")
         return render(request,'common/emailsendsuccess.html')
    return render(request,'common/password_reset_form.html')

def password_reset_confirm(request, uidb64, token):
        User=get_user_model()
        try:
          uid = force_str(urlsafe_base64_decode(uidb64))
          user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            print(user)
        if user is not None and default_token_generator.check_token(user,token):
             if request.method == 'POST':
                  password1=request.POST.get('newpass')
                  password2=request.POST.get('confpass')

                  if password1 == password2:
                      user.password = make_password(password1)
                      user.save()
                      messages.success(request,'your password has been reset')
                      return redirect('home')
                  else:
                      messages.error(request,'password do not match')
                      return render(request,'common/password_reset_confirm.html')
                      
                          
             return render(request,'common/password_reset_confirm.html')
        else:
           return render(request,'common/password_reset_form.html')
    

def vall(request):
    
    if request.user.is_authenticated:
        if request.user.groups.filter(name='CUSTOMER').exists():
            return redirect('userhome')
       
    return redirect('login')