from django.shortcuts import render
from django.views import View
from .forms import AddMoviesForm
from .models import *


class AddMovies(View):
    def get(self, request):
        form = AddMoviesForm()
        return render(request, "add_movies.html", {"form": form})

    def post(self, request):
        data = AddMoviesForm(request.POST, request.FILES)
        if data.is_valid():
            datanew = data.cleaned_data.get("movie_genre", [])
        # movie_name = request.POST["movie_name"]
        # movie_genre = request.POST.cleaned_data.get("movie_genre", [])
        # movie_cast = request.POST["movie_cast"]
        return render(request, "add_movies.html", {"data": (data, datanew)})


class MoviesPage(View):
    def get(self, request):
        movie_genre = Genres.objects.all().order_by("genre_name").values()
        languages = Language.objects.all()
        movies = Movies.objects.all()

        return render(request, "movies.html", {"movie_genres": movie_genre, "movies": movies, "movie_language": languages})


class SelectMovie(View):
    def get(self, request, id):
        movie_data = Movies.objects.get(id=id)
        return render(request, "selected_movies.html", {"movie": movie_data})


class GenrePage(View):
    def get(self, request):
        genres = Genres.objects.all()
        return render(request, "genres.html", {"genres": genres})
