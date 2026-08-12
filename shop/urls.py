from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .forms import UzbekLoginForm
from .views import *
urlpatterns=[
path("",home,name="home"),
path("mahsulot/<slug:slug>/",product_detail,name="product"),
path("savat/",cart,name="cart"),
path("savat/qoshish/<int:pk>/",add_cart,name="add_cart"),
path("savat/ochirish/<int:pk>/",remove_cart,name="remove_cart"),
path("buyurtma/",checkout,name="checkout"),
path("buyurtma/tayyor/<int:pk>/",order_success,name="order_success"),
path("buyurtmalar/",orders,name="orders"),
path("login/",LoginView.as_view(template_name="login.html", authentication_form=UzbekLoginForm),name="login"),
path("logout/",LogoutView.as_view(next_page="/"),name="logout"),
path("register/",register,name="register"),
]
