from django.urls import path
from .views import *


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
]
