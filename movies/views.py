from django.db.models import Avg
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import get_object_or_404
from .forms import *
from .models import *
import os


class AddMovies(View):
    def get(self, request):
        form = AddMoviesForm()
        return render(request, "add_movies.html", {"form": form})

    def post(self, request):
        movie_image = request.FILES["movie_images"]
        movie_poster = request.FILES.get("movie_poster")
        movie_genre = request.POST.getlist("movie_genre")
        movie_cast = request.POST.getlist("movie_cast")
        movie_release = request.POST["movie_release"]
        movie_writer = request.POST["movie_writer"]
        movie_budget = request.POST["movie_budget"]
        movie_name = request.POST["movie_name"]
        movie_length = request.POST["movie_length"]
        movie_director = request.POST["movie_director"]
        movie_plot = request.POST["movie_plot"]
        movie_language = request.POST["movie_language"]
        language_instance = Language.objects.get(pk=movie_language)
        reviewer = request.user
        if request.user.is_staff:
            movie_verified = True
        else:
            movie_verified = False

        movie = Movies(movie_name=movie_name, movie_plot=movie_plot,
                       movie_release=movie_release, movie_writer=movie_writer, movie_images=movie_image, movie_poster=movie_poster,
                       movie_budget=movie_budget, movie_length=movie_length, movie_director=movie_director, movie_language=language_instance, movie_verified=movie_verified, movie_uploaded_by=reviewer)
        movie.save()
        movie.movie_genre.set(movie_genre)
        movie.movie_cast.set(movie_cast)
        if request.user.is_staff:
            return redirect("movies")

        return render(request, "base.html")


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


class Verify(View):
    def get(self, request, id):
        movie_id = id
        movie = Movies.objects.get(id=movie_id)
        movie.movie_verified = True
        movie.save()
        return redirect("movies")


def delete_movie(request, id):
    movie = Movies.objects.get(id=id)
    os.remove(movie.movie_images.path)
    os.remove(movie.movie_poster.path)
    movie.delete()
    messages.success(request, "Movie has been deleted.")
    return redirect("home")


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
        movies = Movies.objects.filter(movie_verified=True)

        return render(request, "movies.html", {"movie_genres": movie_genre, "movies": movies, "movie_language": languages})


class FilterMovies(View):
    def post(self, request):
        selected_genre = request.POST.getlist("genre")
        language = request.POST.get("language")

        movie_genre = Genres.objects.all().order_by("genre_name").values()
        languages = Language.objects.all()
        if language:
            if selected_genre is None:

                movies = Movies.objects.filter(
                    movie_language=language).filter(movie_verified=True)
            else:
                movies = Movies.objects.filter(movie_language=language).filter(
                    movie_genre__in=selected_genre).distinct()
        else:
            movies = Movies.objects.filter(
                movie_genre__in=selected_genre).distinct().filter(movie_verified=True)

        return render(request, "movies.html", {"movie_genres": movie_genre, "movies": movies, "movie_language": languages})


class SelectMovie(View):
    def get(self, request, id):
        try:
            movie_data = get_object_or_404(Movies, movie_name=id)

            check = WatchList.objects.filter(
                movies_id=movie_data.id, user=request.user).first()
            # cast = Movies.objects.get("movie_cast")
            cast = People.objects.filter(id__in=Movies.objects.filter(
                movie_name=id).values("movie_cast"))
            rate_review_form = ReviewAndRateForm()
            reviews_rating = ReviewAndRate.objects.filter(movie=movie_data.id)
            if reviews_rating:
                avg_rating = reviews_rating.aggregate(
                    avg_rating=Avg('rating'))['avg_rating']
            else:
                avg_rating = 0
            context = {"movie": movie_data, "cast": cast, "check": check, "rate_review_form": rate_review_form,
                       "reviews_rating": reviews_rating, "rating": round(avg_rating, 1)}
        except:
            return render(request, "base.html", {"error": "error"})

        return render(request, "selected_movies.html", context)

# Search Movies


class Search(View):
    def post(self, request):
        keyword = request.POST["keyword"]

        try:
            movies = Movies.objects.filter(
                movie_name__icontains=keyword).filter(movie_verified=True)
            # rating_avg = movies.annotate(
            # avg_rating=Avg("rating__value")).values("movie_name", "avg_rating")

        except:
            rating_avg = None
        return render(request, "search_results.html", {'keyword': keyword, "movies": movies})


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
        movies = Movies.objects.filter(
            movie_genre=id).filter(movie_verified=True)
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
        peoples = People.objects.all().order_by("actors_name")
        paginator = Paginator(peoples, 8)
        page_number = request.GET.get("page")
        people = paginator.get_page(page_number)
        numbers = people.paginator.num_pages*"a"
        return render(request, "people.html", {"people": people, "numbers": numbers})

    def post(self, request):
        keyword = request.POST["actor"]
        people = People.objects.filter(actors_name__contains=keyword)
        return render(request, "people.html", {"people": people, "keyword": keyword})


class Actors(View):
    def get(self, request, id):
        actor = People.objects.get(id=id)
        movies = Movies.objects.filter(
            movie_cast=id).filter(movie_verified=True)
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
