from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from .forms import UzbekRegisterForm
from django.db.models import Q
from django.contrib import messages
from .models import Category,Product,Cart,CartItem,Order,OrderItem,Favorite
from django.conf import settings
from .demo_data import seed_demo_data

def home(request):
    # Local/demo convenience: if the freshly migrated database is empty,
    # populate it once so the marketplace is immediately visible.
    if getattr(settings, "DEBUG", False) and not Product.objects.exists():
        seed_demo_data()
    q=request.GET.get("q","").strip()
    cat=request.GET.get("category","")
    products=Product.objects.filter(is_active=True)
    if q: products=products.filter(Q(name__icontains=q)|Q(description__icontains=q))
    if cat: products=products.filter(category__slug=cat)
    return render(request,"home.html",{"products":products,"categories":Category.objects.all(),"q":q,"cat":cat})

def product_detail(request,slug):
    p=get_object_or_404(Product,slug=slug,is_active=True)
    return render(request,"product.html",{"product":p})

def add_cart(request,pk):
    if not request.user.is_authenticated:
        messages.info(request,"Savatdan foydalanish uchun avval ro'yxatdan o'ting.")
        return redirect("register")
    p=get_object_or_404(Product,pk=pk,is_active=True)
    cart,_=Cart.objects.get_or_create(user=request.user)
    item,_=CartItem.objects.get_or_create(cart=cart,product=p)
    item.quantity=min(item.quantity+1,p.stock); item.save()
    return redirect("cart")

def cart(request):
    if not request.user.is_authenticated:
        messages.info(request,"Savatdan foydalanish uchun avval ro'yxatdan o'ting.")
        return redirect("register")
    c,_=Cart.objects.get_or_create(user=request.user)
    return render(request,"cart.html",{"cart":c})

@login_required
def remove_cart(request,pk):
    CartItem.objects.filter(pk=pk,cart__user=request.user).delete()
    return redirect("cart")

@login_required
def checkout(request):
    c,_=Cart.objects.get_or_create(user=request.user)
    items=list(c.items.select_related("product"))
    if not items:
        messages.warning(request,"Savatcha bo'sh."); return redirect("home")
    if request.method=="POST":
        o=Order.objects.create(user=request.user,full_name=request.POST["full_name"],phone=request.POST["phone"],address=request.POST["address"])
        total=0
        for i in items:
            OrderItem.objects.create(order=o,product=i.product,quantity=i.quantity,price=i.product.price)
            total+=i.total
            i.product.stock=max(0,i.product.stock-i.quantity); i.product.save()
        o.total=total; o.save(); c.items.all().delete()
        return redirect("order_success",o.id)
    return render(request,"checkout.html",{"items":items})

@login_required
def order_success(request,pk):
    o=get_object_or_404(Order,pk=pk,user=request.user)
    return render(request,"success.html",{"order":o})

def register(request):
    if request.method=="POST":
        f=UzbekRegisterForm(request.POST)
        if f.is_valid():
            user=f.save(); login(request,user); return redirect("home")
    else: f=UzbekRegisterForm()
    return render(request,"register.html",{"form":f})

@login_required
def orders(request):
    return render(request,"orders.html",{"orders":request.user.orders.all()})
