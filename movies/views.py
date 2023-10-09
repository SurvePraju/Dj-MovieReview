from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from .forms import AddMoviesForm
from .models import *


class AddMovies(View):
    def get(self, request):
        form = AddMoviesForm()
        return render(request, "add_movies.html", {"form": form})

    def post(self, request):

        movie_name = request.POST["movie_name"]
        movie_poster = request.FILES["movie_poster"]
        movie_images = request.FILES["movie_images"]
        movie_plot = request.POST["movie_plot"]
        movie_length = request.POST["movie_length"]
        movie_release = request.POST["movie_release"]
        movie_director = request.POST["movie_director"]
        movie_writer = request.POST["movie_writer"]
        movie_budget = request.POST["movie_budget"]
        movie_genre = [genre for genre in request.POST.get("movie_genre")]
        movie_cast = request.POST.getlist("movie_cast")
        movie_language = request.POST["movie_language"]
        movie = [
            movie_genre,
            movie_cast,
            movie_language]
        # if data.is_valid():
        #     data.save()
        # genre = request.POST["movie_genre"]
        # cast = request.POST["movie_cast"]

        # data.movie_genre.add(genre)
        # data.movie_cast.add(cast)
        return render(request, "add_movies.html", {"data": movie})


class MoviesPage(View):
    def get(self, request):
        movie_genre = Genres.objects.all().order_by("genre_name").values()
        languages = Language.objects.all()
        movies = Movies.objects.all()

        return render(request, "movies.html", {"movie_genres": movie_genre, "movies": movies, "movie_language": languages})


class SelectMovie(View):
    def get(self, request, id):
        movie_data = Movies.objects.get(movie_name=id)
        check = WatchList.objects.filter(
            movies_id=movie_data.id, user=request.user).first()
        # cast=Movies.objects.get(movie_cast)
        cast = Movies.objects.filter(movie_name=id)
        return render(request, "selected_movies.html", {"movie": movie_data, "cast": movie_data.movie_cast, "check": check})


class GenrePage(View):
    def get(self, request):
        try:
            genres = Genres.objects.all()
        except:
            genres = None
            # return None
        return render(request, "genres.html", {"genres": genres})


class AddWatchlist(View):
    def post(self, request, movie_id):

        data = WatchList.objects.filter(
            movies_id=movie_id, user=request.user).first()
        if data is None:
            data = WatchList(movies_id=movie_id, user=request.user)
            data.save()
            messages.success(
                request, f"{data.movies} is added to your watchlist")
        else:
            data.delete()
            messages.success(
                request, f"{data.movies} is deleted to your watchlist")
        return redirect(request.META.get("HTTP_REFERER"))


class ActorsPage(View):
    def get(self, request):
        people = People.objects.all()
        return render(request, "people.html", {"people": people})
