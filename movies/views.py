from django.shortcuts import render, redirect
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
