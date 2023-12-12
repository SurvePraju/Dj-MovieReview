# Create your views here.
from django.contrib.auth.forms import PasswordChangeForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import Profile as ProfilePictureModel
from movies.models import WatchList, Movies, Genres


# Create your views here.


class LoginRequired(LoginRequiredMixin):
    login_url = "/login/"

    def handle_no_permission(self) -> HttpResponseRedirect:
        return HttpResponseRedirect(self.login_url)


class Home(View):
    def get(self, request):
        movies = Movies.objects.filter(
            movie_verified=True)
        unverified_movies = Movies.objects.filter(movie_verified=False)
        latest = movies.order_by("-movie_date_uploaded")
        trending = movies.order_by("-movie_visited")
        genres = Genres.objects.all().order_by("genre_name")[:10]
        avg_rating_movie = Movies.objects.annotate(
            avg_ratings=Avg("reviewandrate__rating")).order_by("-avg_ratings")

        context = {"movies": movies[:10], "unverified_movies": unverified_movies,
                   "latest": latest[:8], "trending": trending, "genres": genres, "avg": avg_rating_movie}
        return render(request, "home.html", context)

    def post(self, request):
        pass


class Register(View):
    def get(self, request):
        context = {}
        context["form"] = UserRegistrationForm()
        return render(request, "register.html", context)

    def post(self, request):

        user_data = UserRegistrationForm(request.POST)
        # password = request.POST["password2"]
        # username = request.POST["username"]
        if user_data.is_valid():
            user_data.save()

            # login(request, username, password)
            messages.success(request, "Registration Successfull !")
            return redirect("login")
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
        try:
            exits = User.objects.get(username=username)

            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"User {username} Logged in Succesfully! ")
                return redirect("home")
            else:
                messages.warning(
                    request, f"Incorrect Password !!")
            return redirect("login")
        except:
            messages.warning(
                request, f"User is Not Registered ")
            return redirect("login")


def user_logout(request):

    if request.user.is_authenticated:
        logout(request)
        messages.success(
            request, f"User {request.user.username} Logged Off Succesfully!")
        return redirect("login")


class Profile(LoginRequired, View):
    def get(self, request):

        active = request.GET.get("active")

        if active == None:
            active = 1

        form = UpdateUser(instance=request.user)
        try:
            profile_form = ProfilePicture(instance=request.user.profile)
        except:
            profile_form = ProfilePicture()
        change_password = ChangePassword(request.user)
        watchlist = WatchList.objects.filter(
            user=request.user).values_list("movies", flat=True)
        movieslist = []
        for item in list(watchlist):
            movies = Movies.objects.get(id=item)
            movieslist.append(movies)

        return render(request, "profile.html", {"profile_form": profile_form, "form": form, "active": int(active), "movies": movieslist, "change_password_form": change_password})

    def post(self, request):

        user_form = UpdateUser(request.POST, instance=request.user)
        try:
            profile = ProfilePictureModel.objects.get(reviewer=request.user)
        except:
            profile = None

        profile_picture_form = ProfilePicture(
            request.POST, request.FILES, instance=profile) if profile else ProfilePicture(request.POST, request.FILES)

        if user_form.is_valid() and profile_picture_form.is_valid():
            user_form.save()

            if profile:
                profile.profile_picture = profile_picture_form.cleaned_data['profile_picture']
            else:
                profile = ProfilePictureModel(
                    reviewer=request.user, profile_picture=profile_picture_form.cleaned_data['profile_picture'])
            profile.save()

        return redirect('profile')


class ChangePasswordView(View):
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
