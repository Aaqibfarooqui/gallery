from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import pro,cont,cart,order
from django.db.models import Q
import random
import razorpay

# Create your views here.

    
def gallery(request):
    return render(request,'gallery.html')

def single(request):
    return render(request,'gallery-single.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

# def abouts(request):
#     return render(request,'abouts.html')

def services(request,rid):
    p=pro.objects.filter(id=rid)
    c={}
    c['data']=p
    return render(request,'services.html',c)

def contact(request):
    if request.method=='POST':
        n=request.POST['name']
        o=request.POST['email']
        p=request.POST['subject']
        q=request.POST['message']
        u=cont.objects.create(customer_name=n,customer_email=o,customer_concern=p,customer_message=q)
        u.save()
        c={}
        c['data']="We have received your request...."
        return render(request,'contact.html',c)
    else:
        return render(request,'contact.html')
        
   
def user_login(request):    
    if request.method=="POST":
        uname=request.POST["uname"]
        upass=request.POST["upass"]
        
        if uname=="" or upass=="":
            context={}
            context['errmsg']="field can not be empty"
            return render(request,'login.html',context)
        
        else:
            u=authenticate(username=uname,password=upass)
            # print(u)
            # login(u)
            if u is not None:
                login(request,u)
                #login
            #return HttpResponse("in else part")
                return redirect('/index')
            
            else:
                context={}
                context['errmsg']="Invalid Username and password"
                return render(request,'login.html',context)

    else:
        return render(request,'login.html')

# def register(request):
#     return render(request,'register.html')

def register(request):
    if request.method=="POST":
        name=request.POST['uname']
        mail=request.POST['email']
        cont=request.POST['ucontact']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        
        if mail=="" or upass=="" or ucpass=="":
            context={}
            context['errmsg']="field cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context={}
            context['errmsg']="Plz check your password"
            return render(request,'register.html',context)
           
        else:
            u=User.objects.create(username=name,email=mail,password=upass)
            u.set_password(upass)
            u.save()
            context={}
            context['success']="User created successfully!!"
            #return render('data is fetch successfully!!')
            return redirect("/login")
            
            # except Exception:
            #     context={}
            #     context['errmsg']="User name already exists"
            #     return render(request,'register.html',context)


    else:
        return render(request,'register.html')
    
def user_logout(request):
    logout(request)
    return redirect('/index')

def index(request):
    c={}
    p=pro.objects.filter(is_active=True)
    c['data']=p
    return render(request,'index.html',c)

def filter(request,pid):
    a=Q(is_active=True)
    b=Q(Categories=pid)
    c=pro.objects.filter(a and b)
    d={}
    d['data']=c
    return render(request,'index.html',d)

def sort(request,sv):
    if sv== '0':
        col = 'price' #asc

    else:
        col = '-price' #decending

    p=pro.objects.order_by(col)
    d={}
    d['data']=p
    return render(request,'index.html',d)

def addtocart(request,pid):
    userid=request.user.id
    u=User.objects.filter(id=userid)
    print(u[0])
    p=pro.objects.filter(id=pid)
    print(p[0])
    q1=Q(uid=u[0])
    q2=Q(pid=p[0])
    c=cart.objects.filter(q1 and q2)
    n=len(c)
    print(n )
    context={}
    context['data']=p
    if n==1:
        context['msg']='product already exist!!'
    
    else:   
        c=cart.objects.create(uid=u[0],pid=p[0])
        c.save()
        context={}
        context['data']=p
        context['success']='Product added successfully in the cart !!!!!!!!!!!!!!'
    
    # print(pid)
    # print(userid)
    # return HttpResponse("id is fetched")
    return render(request,'services.html',context)

def viewcart(request):
    # r=request.user.id
    if request.user.is_authenticated:
        c=cart.objects.filter(uid=request.user.id)
        np=len(c)
        s=0
        for x in c:
        # print(x.pid.price)
            s=s+x.pid.price*x.qty

    # print(s)
        context={}
        context['data']=c
        context['total']=s
        context['n']=np
        return render(request,'cart.html',context)
    else:
        return redirect('/login')
    
def remov(request,cid):
    c=order.objects.filter(id=cid)
    print(c)
    c.delete()
    return redirect('/placeorder')
    # return HttpResponse("Hii")

def updateqty(request,cid,sv):
    c=cart.objects.filter(id=cid)
    # print(c)
    # print(c[0])
    # print(c[0].qty)
    if sv == '1':
        t=c[0].qty+1
        c.update(qty=t)

    else:
        if c[0].qty> 1:
            t=c[0].qty-1
            c.update(qty=t)

   
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    # print(userid)
    c=cart.objects.filter(uid=userid)
    # print(c)
    oid=random.randrange(1000,9999)
    # print(oid)
    for x in c:
        # print(x)
        # print(x.pid)
        # print(x.qty)
        o=order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()#save data into order table
        x.delete()#delete records for cart table
    
    orders=order.objects.filter(uid=userid)
    np=len(orders)
    s=0
    for x in orders:
        # print(x.pid.price)
        s=s+x.pid.price*x.qty

    print(s)
    context={}
    context['data']=orders
    context['total']=s
    context['n']=np
    
    # return HttpResponse('Order place successfully!!!')
    return render(request,'placeorder.html',context)

def makepayment(request):
    orders=order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        # print(x.pid.price)
        s=s+x.pid.price*x.qty
   

        oid=x.order_id
    # print(s)
    client = razorpay.Client(auth=("rzp_test_GjYspfqzYfXGjO", "AKC2LhojZreKphpd1FwurvqK"))

    DATA = {
    "amount": s * 100,
    "currency": "INR",
    "receipt": oid,
    "notes": {
        "key1": "value3",
        "key2": "value2"
       }
    }
    payment=client.order.create(data=DATA)
    
    print(payment)
    uname=request.user.username
    print(uname)
    context={}
    context['orders']=payment
    context['uname']=uname
    client.order.create(data=DATA)
    # return HttpResponse('in payment section')
    return render(request,'pay.html',context)