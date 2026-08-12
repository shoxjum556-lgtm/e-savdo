from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=120)
    slug=models.SlugField(unique=True)
    image=models.ImageField(upload_to="categories/",blank=True,null=True)
    def __str__(self): return self.name
    class Meta: verbose_name="Kategoriya"; verbose_name_plural="Kategoriyalar"

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    name=models.CharField(max_length=220)
    slug=models.SlugField(unique=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=12,decimal_places=2)
    old_price=models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True)
    image=models.ImageField(upload_to="products/",blank=True,null=True)
    stock=models.PositiveIntegerField(default=0)
    rating=models.DecimalField(max_digits=3,decimal_places=1,default=5)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return round((self.old_price - self.price) * 100 / self.old_price)
        return 0

    class Meta:
        ordering=["-created_at"]
        verbose_name="Mahsulot"; verbose_name_plural="Mahsulotlar"

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    class Meta: unique_together=("cart","product")
    @property
    def total(self): return self.product.price*self.quantity

class Order(models.Model):
    STATUS=[("new","Yangi"),("confirmed","Tasdiqlangan"),("shipped","Yetkazilmoqda"),("done","Yakunlangan"),("cancelled","Bekor qilingan")]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    full_name=models.CharField(max_length=160)
    phone=models.CharField(max_length=30)
    address=models.CharField(max_length=300)
    status=models.CharField(max_length=20,choices=STATUS,default="new")
    total=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"#{self.id} — {self.full_name}"
    class Meta:
        ordering=["-created_at"]
        verbose_name="Buyurtma"; verbose_name_plural="Buyurtmalar"

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=12,decimal_places=2)
    @property
    def total(self): return self.price*self.quantity

class Favorite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="favorites")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    class Meta: unique_together=("user","product")
