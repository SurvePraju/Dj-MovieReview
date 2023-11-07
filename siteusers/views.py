# Create your views here.
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.db.models import Avg
from django.views import View
from .forms import *
from movies.models import WatchList, Movies, Genres

# Create your views here.


class Home(View):
    def get(self, request):
        movies = Movies.objects.filter(
            movie_verified=True)
        unverified_movies = Movies.objects.filter(movie_verified=False)
        latest = movies.order_by("-movie_date_uploaded")
        genres = Genres.objects.all()
        avg_rating_movie = Movies.objects.annotate(
            avg_ratings=Avg("reviewandrate__rating")).order_by("-avg_ratings")

        context = {"movies": movies[:10], "unverified_movies": unverified_movies,
                   "latest": latest[:8], "genres": genres, "avg": avg_rating_movie}
        return render(request, "home.html", context)

    def post(self, request):
        pass


class Register(View):
    def get(self, request):
        context = {}
        context["form"] = UserRegistrationForm()
        return render(request, "register.html", context)

    def post(self, request):
        # context = {}
        # context["form"] = UserRegistrationForm()
        user_data = UserRegistrationForm(request.POST)
        if user_data.is_valid():
            user_data.save()
            messages.success(request, "Registration Successfull !")
            return redirect("home")
        else:
            # return render(request, "register.html", context)
            messages.warning(request, "Registration Unsuccesfull Try Again")
            return redirect("register")


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
    def get(self, request):

        active = request.GET.get("active")
        if active == None:
            active = 1
        form = UserRegistrationForm()
        change_password = ChangePassword(request.user)
        watchlist = WatchList.objects.filter(
            user=request.user).values_list("movies", flat=True)
        movieslist = []
        for item in list(watchlist):
            movies = Movies.objects.get(id=item)
            movieslist.append(movies)

        # form = ChangePassword()
        # watchlist = Movies.objects.filter(watchlist=request.user.id)

        return render(request, "profile.html", {"form": form, "active": int(active), "movies": movieslist, "change_password_form": change_password})

    def post(self, request):
        change_password = ChangePassword(request.user, request.POST)
        if change_password.is_valid():
            change_password.save()
            update_session_auth_hash(request, change_password)
            return redirect('profile')
        else:
            messages.warning(request,
                             "Password Change Unsuccesful Something went wrong ")
            return redirect("profile")
