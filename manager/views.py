from django.shortcuts import render,redirect,get_object_or_404
from .models import category,perfume,rating
from user.models import Register,Order,OrderItem
from django.contrib import messages
def home(request):
    p=perfume.objects.all()[:5]
    return render(request,'common/home.html',{'data':p})

def managerhome(request):
    return render(request,'manager/managerhome.html')



def catgry(request):
    if request.method=='POST':
        cate=request.POST.get('cate')

        s=category.objects.create(category=cate)
        s.save()
        return redirect('home')
    return render(request,'manager/cat.html')


def rate(request):
    if request.method=='POST':
        rat=request.POST.get('rate')
        s=rating.objects.create(rating=rat)
        s.save()
        return redirect('rate')
    return render(request,'manager/rate.html')

def perfumes(request):
    c=category.objects.all()
    if request.method=='POST':
        pname=request.POST.get('pname')
        pbrand=request.POST.get('pbrand')
        pdetails=request.POST.get('pdetails')
        pprice=request.POST['pprice']
        pimage=request.FILES.get('pimage')
        pstock=request.POST.get('pstock')
        pscent=request.POST.get('pscent')
        pvolume=request.POST.get('pvolume')
        pcategoryid=request.POST.get('pcatid')
        

        k=perfume.objects.create(perfumename=pname,perfumebrand=pbrand,
                                 perfume_details=pdetails,perfume_price=pprice,
                                 perfume_image=pimage,perfume_stock=pstock,
                                 perfume_scent=pscent,perfume_volume=pvolume,
                                 perfume_category_id=pcategoryid
                                 )
        k.save()
        return redirect('perfume')
    return render(request,'manager/add_perfume.html',{'data':c})

def viewperfume(request):
    t=perfume.objects.all()
    return render(request,'manager/perfumetable.html',{'data':t})

def deleteperfume(request,id):
    perfume.objects.filter(id=id).delete()
    return redirect('viewperfume')

def editperfume(request,id):
    ed=get_object_or_404(perfume,id=id)
    c=category.objects.all()
    if request.method=='POST':
        ed.perfumename=request.POST.get('pname')
        ed.perfumebrand=request.POST.get('pbrand')
        ed.perfume_details=request.POST.get('pdetails')
        ed.perfume_price=request.POST.get('pprice')
        if 'perfume_pic' in request.FILES:
            ed.perfume_image=request.FILES['perfume_image']
        ed.perfume_stock=request.POST.get('pstock')
        ed.perfume_scent=request.POST.get('pscent')
        ed.perfume_volume=request.POST.get('pvolume')
        ed.perfume_category_id=request.POST.get('pcatid')
        ed.save()
        return redirect('viewperfume')
    return render(request,'manager/editperfume.html',{'data':ed,'user':c})



def viewregister(request):
    a=Register.objects.all()
    return render(request,'common/viewreg.html',{'data':a})

def vieworders(request):
    status=request.GET.get('status')
    if status == 'pending':
        o=Order.objects.filter(orderstatus='pending')
    elif status == 'all':
        o=Order.objects.all()
    elif status =='Processed':
        o=Order.objects.filter(orderstatus='Processed')
    elif status =='Completed':
        o=Order.objects.filter(orderstatus='Completed')
    elif status =='Cancelled':
        o=Order.objects.filter(orderstatus='Cancelled')
    else:
        o=Order.objects.all()
        
    return render(request,'manager/vorders.html',{'data':o})

def adminorderdetails(request,id):
    ed=get_object_or_404(Order,id=id)
    g=OrderItem.objects.filter(order_id=ed.id)
    return render(request,'manager/vadminorderdetails.html',{'data':ed,'data1':g})

def orderupdate(request,id):
    if request.method=='POST':
        carrier=request.POST.get('carr')
        tracking=request.POST.get('tid')
        deliverydate=request.POST.get('ddate')
        
        Order.objects.filter(id=id).update(Carrier=carrier,trackingid=tracking,deliverydate=deliverydate,orderstatus='Processed')
        messages.success(request,'Successfully Updated')
        return redirect('vorders')

def Completeadmin(request,id):
    if request.method=='POST':
        Order.objects.filter(id=id).update(orderstatus='Completed',paymentstatus='Completed')
        return redirect('vorders')
def Canceladmin(request,id):
    if request.method=='POST':
        Order.objects.filter(id=id).update(orderstatus='Cancelled',paymentstatus='Failed')
        return redirect('vorders')