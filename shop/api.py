from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Category,Product,Cart,CartItem,Order,Favorite
from .serializers import *

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.filter(is_active=True).select_related("category")
    serializer_class=ProductSerializer
    def get_queryset(self):
        qs=super().get_queryset()
        q=self.request.query_params.get("q")
        category=self.request.query_params.get("category")
        if q: qs=qs.filter(Q(name__icontains=q)|Q(description__icontains=q))
        if category: qs=qs.filter(category__slug=category)
        return qs

class CartViewSet(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated]
    def list(self,request):
        cart, _=Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)
    def create(self,request):
        product=Product.objects.get(pk=request.data.get("product_id"),is_active=True)
        qty=max(1,int(request.data.get("quantity",1)))
        cart,_=Cart.objects.get_or_create(user=request.user)
        item,_=CartItem.objects.get_or_create(cart=cart,product=product)
        item.quantity=min(item.quantity+qty,product.stock); item.save()
        return Response(CartSerializer(cart).data,status=status.HTTP_201_CREATED)
    def destroy(self,request,pk=None):
        CartItem.objects.filter(cart__user=request.user,pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OrderSerializer
    def get_queryset(self): return Order.objects.filter(user=self.request.user).prefetch_related("items__product")

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    s=RegisterSerializer(data=request.data); s.is_valid(raise_exception=True); user=s.save()
    token=RefreshToken.for_user(user)
    return Response({"user":s.data,"access":str(token.access_token),"refresh":str(token)})

class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=FavoriteSerializer
    def get_queryset(self): return Favorite.objects.filter(user=self.request.user)
    def perform_create(self,serializer): serializer.save(user=self.request.user)
