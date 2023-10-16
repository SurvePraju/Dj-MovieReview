from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views import View
from .forms import *
from .models import *
import os


class AddMovies(View):
    def get(self, request):
        form = AddMoviesForm()
        return render(request, "add_movies.html", {"form": form})

    def post(self, request):

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


class AddGenres(View):
    def get(self, request):
        add_genres_form = AddGenresForm()
        return render(request, "add_genre.html", {"add_genre": add_genres_form})

    def post(self, request):
        name = request.POST["genre_name"]
        genre_data = AddGenresForm(request.POST, request.FILES)
        if genre_data.is_valid():
            genre_data.save()
            messages.success(request, f"{name} Genres has been Added")
        else:
            messages.warning(
                request, f"{name} Already Exists !!")
        return redirect("genres")


class Addactors(View):
    def get(self, request):
        add_genres_form = AddActorsForm()
        return render(request, "add_actor.html", {"add_actors": add_genres_form})

    def post(self, request):
        name = request.POST["actors_name"]
        actor_data = AddActorsForm(request.POST, request.FILES)
        if actor_data.is_valid():
            actor_data.save()
            messages.success(request, f"{name} Actors has been Added")
        else:
            messages.warning(
                request, f"{name} Already Exists !!")
        return redirect("actors")


def delete_genre(request, id):

    genre = Genres.objects.get(id=id)
    os.remove(genre.genre_images.path)
    genre.delete()
    messages.success(request, f"{genre} Deleted Succesfully")
    return redirect("genres")


def delete_actor(request, id):

    actor = People.objects.get(id=id)
    if actor is not None:
        os.remove(actor.actors_images.path)
        actor.delete()
        messages.success(request, f"Actor has been Deleted/")
        return redirect("actors")
    else:
        return redirect("home")


class MoviesPage(View):

    def get(self, request):
        movie_genre = Genres.objects.all().order_by("genre_name").values()
        languages = Language.objects.all()
        movies = Movies.objects.all()

        return render(request, "movies.html", {"movie_genres": movie_genre, "movies": movies, "movie_language": languages})


class FilterMovies(View):
    def post(self, request):
        selected_genre = request.POST.getlist("genre")
        language = request.POST.getlist("language")
        movie_genre = Genres.objects.all().order_by("genre_name").values()
        languages = Language.objects.all()
        if language:
            if selected_genre is None:

                movies = Movies.objects.filter(movie_language=language)
            else:
                movies = Movies.objects.filter(movie_language=language).filter(
                    movie_genre__in=selected_genre).distinct()
        else:
            movies = Movies.objects.filter(
                movie_genre__in=selected_genre).distinct()

        return render(request, "movies.html", {"movie_genres": movie_genre, "movies": movies, "movie_language": languages})


class SelectMovie(View):
    def get(self, request, id):
        movie_data = Movies.objects.get(movie_name=id)
        check = WatchList.objects.filter(
            movies_id=movie_data.id, user=request.user).first()
        # cast = Movies.objects.get("movie_cast")
        cast = People.objects.filter(id__in=Movies.objects.filter(
            movie_name=id).values("movie_cast"))
        rate_review_form = ReviewAndRateForm()
        reviews_rating = ReviewAndRate.objects.filter(movie=movie_data.id)
        return render(request, "selected_movies.html", {"movie": movie_data, "cast": cast, "check": check, "rate_review_form": rate_review_form, "reviews_rating": reviews_rating})


class GenrePage(View):
    def get(self, request):
        try:
            genres = Genres.objects.all()
        except:
            genres = None
            # return None
        return render(request, "genres.html", {"genres": genres})


class SelectedGenre(View):
    def get(self, request, id):
        genre = Genres.objects.get(id=id)
        movies = Movies.objects.filter(movie_genre=id)
        return render(request, "genre_movies.html", {"genre": genre, "movies": movies})


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


class Actors(View):
    def get(self, request, id):
        actor = People.objects.get(id=id)
        movies = Movies.objects.filter(movie_cast=id)
        return render(request, "actor.html", {"actor": actor, "movies": movies})


class Reviews(View):
    def post(self, request, id):
        review_data = request.POST["review"]
        rating_data = request.POST["rating"]
        viewer = request.user
        movie = Movies.objects.get(id=id)
        save_review = ReviewAndRate(
            viewer=viewer, rating=rating_data, review=review_data, movie=movie)
        save_review.save()
        messages.success(request, "Review Added Succesfully")
        return redirect(request.META.get("HTTP_REFERER"))
