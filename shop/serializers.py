from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category,Product,Cart,CartItem,Order,OrderItem,Favorite

class CategorySerializer(serializers.ModelSerializer):
    class Meta: model=Category; fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(source="category.name",read_only=True)
    class Meta: model=Product; fields="__all__"

class CartItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    total=serializers.DecimalField(max_digits=12,decimal_places=2,read_only=True)
    class Meta: model=CartItem; fields=("id","product","quantity","total")

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    class Meta: model=Cart; fields=("id","items")

class OrderItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source="product.name",read_only=True)
    class Meta: model=OrderItem; fields=("id","product","product_name","quantity","price")

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    class Meta: model=Order; fields=("id","full_name","phone","address","status","total","created_at","items")

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta: model=User; fields=("username","first_name","last_name","email","password")
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta: model=Favorite; fields="__all__"
