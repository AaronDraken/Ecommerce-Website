from django.shortcuts import render,redirect
from .models import Product,User,Cart,Order,Address
from django.views.generic import DetailView
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import reg
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import razorpay
import random
from django.core.mail import send_mail


# Create your views here.
def home(req):
    m=Product.objects.all()
    user=req.user
    if user.is_authenticated:
        cartCount=Cart.objects.filter(user=user).count()
        context={'products':m,'cartCount':cartCount}
    else:
        context={'products':m}
    return render(req,'index.html',context)

class Details(DetailView):
    model=Product
    template_name='details.html'

def filter_mob(req):
    queryset=Product.filter.mobile()
    return render(req,'index.html',{'products':queryset})
def filter_lap(req):
    queryset=Product.filter.laptop()
    return render(req,'index.html',{'products':queryset})
def filter_tv(req):
    queryset=Product.filter.tv()
    return render(req,'index.html',{'products':queryset})

def range(req):
    if req.method == 'GET':
        return redirect('/')
    else:
        try:
            min=req.POST['min']
            max=req.POST['max']
            products=Product.objects.filter(price__range=(min,max))
            return render(req,'index.html',{'products':products})
        except:
            products=Product.objects.all()
            msg='Enter both values to filter'
            return render(req,'index.html',{"products":products,"msg":msg})

def sortProds(req):
    if req.GET.get('sort') == 'asc':
        products=Product.objects.all().order_by('price')
    else:
        products=Product.objects.all().order_by('-price')
    return render(req,'index.html',{'products':products})

def search(req):
    if req.method == 'POST':
        query=req.POST.get('search')
        res=Product.objects.filter(Q(pname__icontains = query)|Q(desc__icontains = query))
        return render(req,'index.html',{'products':res})
    
def addToCart(req,pk):
    p=Product.objects.get(pid=pk)
    if req.user.is_authenticated:
        currUser=req.user 
    else:
        messages.error(req,'Login to access your cart')
        return redirect('/login')
    # METHOD 1 (MANUAL)
    # c=Cart.objects.filter(pid=p)
    # if len(c) == 0:
    #     Cart.objects.create(pid=p)
    # else:
    #     qty=Cart.objects.get(pid=p)
    #     q=qty.quantity+1
    #     c.update(quantity=q)

    # METHOD 2 (Function-based)
    c,created=Cart.objects.get_or_create(pid=p,user=currUser)
    if not created:
        c.quantity+=1
    c.save()
    return redirect('/Cart')

def cart(req):
    if req.user.is_authenticated:
        currUser=req.user
        prod=Cart.objects.filter(user=currUser)
    else:
        messages.error(req,'Login to access your cart')
        return redirect('/login')
        
    sum=0
    for x in prod:
        val=x.quantity * x.pid.price
        sum=sum+val
    return render(req,'cart.html',{'cart':prod,'sum':sum})

def deleteFromCart(req,pk):
    p=Product.objects.get(pid=pk)
    Cart.objects.get(pid=p,user=req.user).delete()
    return redirect('/Cart')

def updateQty(req,btn,pk):
    p=Product.objects.get(pid=pk)
    val=Cart.objects.filter(pid=p)
    quan=Cart.objects.get(pid=p,user=req.user)
    if btn == 0:
        qty=quan.quantity+1
        val.update(quantity=qty)
    else:
        qty=quan.quantity-1
        if qty == 0:
            val.delete()
        else:
            val.update(quantity=qty)
    return redirect('/Cart')

def register(req):
    # form=UserCreationForm     default form
    form=reg()
    if req.method=='POST':
        form=reg(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req,'User created')
            return redirect('/login')
        else:
            messages.error(req,'Invalid user or pass')
    context={'form':form}
    return render(req,'register.html',context)

def loginUser(req):
    if req.method=='POST':
        user=authenticate(req,username=req.POST['uname'],password=req.POST['upass'])
        if user is not None:
            login(req,user)
            req.session['uname']=req.POST['uname']
            return redirect('/')
        else:
            messages.error(req,'Invalid username or password. Try again!')
    return render(req,'login.html')

def logoutUser(req):
    logout(req)
    messages.success(req,'User has Logged Out')
    return redirect('/')

def placeOrder(req):
    currUser=req.user
    prod=Cart.objects.filter(user=currUser)

    sum=0
    for x in prod:
        val=x.quantity * x.pid.price
        sum=sum+val
    return render(req,'placeOrder.html',{'cart':prod,'sum':sum})

def makePayment(req):
    currUser=req.user
    cart=Cart.objects.filter(user=currUser)
    oid=random.randrange(1000,99999)
    for x in cart:
        Order.objects.create(oid=oid,pid=x.pid,quantity=x.quantity,user=x.user)

    client = razorpay.Client(auth=("", ""))
    total_price=0
    for x in cart:
        val=x.quantity * x.pid.price
        total_price+=val
    total_price = total_price * 100 #paise to rs for razorpay
    data = { "amount": total_price, "currency": "INR", "receipt":str(oid) }
    payment = client.order.create(data=data)
    cart.delete()
    

    
    context = {}
    context['data'] = payment
    return render(req,'payment.html',context)

def viewOrder(req):
    order=Order.objects.filter(user=req.user,is_completed=True)
    context={'prods':order}
    return render(req,'orders.html',context)

def genAdd(req):
    add=Address.objects.filter(user=req.user)
    return render(req,'address.html',{'address':add})

def addAdd(req):
    if req.method=='GET':
        return render(req,'addAddress.html')
    else:
        try:
            new_address=req.POST['address']
            new_zip=req.POST['zipcode']
            new_phone=req.POST['phone']
            Address.objects.create(user=req.user,address=new_address,zip=new_zip,phone=new_phone)
            return redirect('/Address')
        except:
            messages.error(req,'Zipcode and/or Phone Number should be an integer not string.')
            return render(req,'addAddress.html')

def updateAdd(req,id):
    add=Address.objects.get(pk=id)
    if req.method=='GET':
        return render(req,'addAddress.html',{'address':add})
    else:
        add.address=req.POST['address']
        add.zip=req.POST['zipcode']
        add.phone=req.POST['phone']
        add.save()
        return redirect('/Address')
    
def delAdd(req,id):
    add=Address.objects.get(pk=id)
    add.delete()
    return redirect('/Address')

def sendUserMail(req):
    try:
        user=User.objects.get(username=req.user)

        print(req.user.email)
        send_mail(
        "Order Places Successfully",
        "Your order has successfully been placed and you should recieve your products in 2-10 days.",
        "",#sender mail
        [""], #reciever mail
        fail_silently=False,
        )
        order=Order.objects.filter(user=req.user,is_completed=False)
        order.update(is_completed=True)

        messages.success(req,'mail sent Successfully')
        return redirect('/')
    except:
        messages.error(req,'Error occured. Couldnt send mail.')
        return redirect('/')
    
def buy(req,pk):
    p=Product.objects.get(pid=pk)
    if req.user.is_authenticated:
        currUser=req.user 
    else:
        messages.error(req,'Login to Place Order')
        return redirect('/login')
    oid=random.randrange(1000,99999)
    Order.objects.create(oid=oid,pid=p,quantity=1,user=currUser)

    client = razorpay.Client(auth=("", ""))
    total_price = p.price * 100 #paise to rs for razorpay
    data = { "amount": total_price, "currency": "INR", "receipt":str(oid) }
    payment = client.order.create(data=data)
    context = {}
    context['data'] = payment
    return render(req,'payment.html',context)
