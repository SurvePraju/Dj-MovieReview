# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views import View
from .forms import *

# Create your views here.


class Home(View):
    def get(self, request):

        return render(request, "home.html")

    def post(self, request):
        pass


class Register(View):
    def get(self, request):
        context = {}
        context["form"] = UserRegistrationForm()
        return render(request, "register.html", context)

    def post(self, request):
        context = {}
        context["form"] = UserRegistrationForm()
        user_data = UserRegistrationForm(request.POST)
        if user_data.is_valid():
            user_data.save()
            return redirect("home")
        else:
            return render(request, "register.html", context)


class Login(View):
    def get(self, request):
        context = {}
        context["form"] = UserLoginForm()
        return render(request, "login.html", context)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, f"User {username} Logged in Succesfully! ")
            return redirect("home")
        else:
            messages.error(
                request, f"User Login Unsuccesfull! ")
        return redirect("login")


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(
            request, f"User {request.user.username} Logged Off Succesfully!")
        return redirect("login")


class Profile(View):
    def get(self, request, active):
        form = UserRegistrationForm()
        # form = ChangePassword()
        return render(request, "profile.html", {"form": form, "active": active})

    def post(self, request):
        return render(request, "profile.html")
