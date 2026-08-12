from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .api import *
router=DefaultRouter()
router.register("categories",CategoryViewSet,basename="category")
router.register("products",ProductViewSet,basename="product")
router.register("cart",CartViewSet,basename="cart")
router.register("orders",OrderViewSet,basename="order")
router.register("favorites",FavoriteViewSet,basename="favorite")
urlpatterns=[
path("",include(router.urls)),
path("auth/register/",register),
path("auth/login/",TokenObtainPairView.as_view()),
path("auth/refresh/",TokenRefreshView.as_view()),
]
