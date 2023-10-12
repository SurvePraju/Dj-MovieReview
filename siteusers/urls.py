from django.urls import path
from .views import *


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", user_logout, name="logout"),
    path("profile/", Profile.as_view(), name="profile"),
]
