from rest_framework import status
from .serializer import MovieSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.views import View
from django.shortcuts import get_object_or_404
from .forms import *
from .models import *
from siteusers.views import LoginRequired
import os


class AddMovies(LoginRequired, View):
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
        else:
            subject = 'Movie Review Aplication'
            message = f'Reviewer {request.user.username} .\n Thank You for contributing by adding a Movies on Movie Review Application, \n It is much Appreciated.  '
            from_email = 'noreply@gmail.com'
            recipient_list = [f'{request.user.email}']

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.send(fail_silently=False)
            return render(request, "base.html")


class UpdateMovie(View):
    def get(self, request, id):
        movie = Movies.objects.get(id=id)
        movie_update_form = AddMoviesForm(instance=movie)
        return render(request, "update_movie.html", {"form": movie_update_form, "movie": movie})

    def post(self, request, id):
        movie = Movies.objects.get(id=id)
        movie_data = AddMoviesForm(request.POST, request.FILES, instance=movie)

        if movie_data.is_valid():

            movie_data.save()

            movie.movie_cast.set(movie_data.cleaned_data['movie_cast'])
            movie.movie_genre.set(movie_data.cleaned_data['movie_genre'])

            return redirect("selected_movie", id=movie)

        return redirect("home")


class AddGenres(LoginRequired, View):
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


class Addactors(LoginRequired, View):
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


class Verify(LoginRequired, View):
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


def delete_review(request, id):
    ReviewAndRate.objects.get(id=id).delete()
    return redirect(request.META.get("HTTP_REFERER"))


class MoviesPage(LoginRequired, View):

    def get(self, request):
        movie_genre = Genres.objects.all().order_by("genre_name").values()
        languages = Language.objects.all()
        movies = Movies.objects.filter(movie_verified=True)

        return render(request, "movies.html", {"movie_genres": movie_genre, "movies": movies, "movie_language": languages})


class FilterMovies(LoginRequired, View):
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


class SelectMovie(LoginRequired, View):
    def get(self, request, id):
        try:
            movie_data = get_object_or_404(Movies, movie_name=id)
            movie_data.movie_visited = models.F("movie_visited")+1
            movie_data.save()

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


class Search(LoginRequired, View):
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


class GenrePage(LoginRequired, View):
    def get(self, request):
        try:
            genres = Genres.objects.all().order_by("genre_name")
        except:
            genres = None
            # return None
        return render(request, "genres.html", {"genres": genres})


class SelectedGenre(LoginRequired, View):
    def get(self, request, id):
        genre = Genres.objects.get(id=id)
        movies = Movies.objects.filter(
            movie_genre=id).filter(movie_verified=True)
        return render(request, "genre_movies.html", {"genre": genre, "movies": movies})


class AddWatchlist(LoginRequired, View):
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


class ActorsPage(LoginRequired, View):
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


class Actors(LoginRequired, View):
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
        try:
            ReviewAndRate.objects.get(movie=movie, viewer=viewer)
            messages.warning(
                request, f"There already exists a Review made by {viewer} for {movie}")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            save_review = ReviewAndRate(
                viewer=viewer, rating=rating_data, review=review_data, movie=movie)
            save_review.save()
            messages.success(request, "Review Added Succesfully")
            return redirect(request.META.get("HTTP_REFERER"))


# API VIEWS


class MoviesAPI(APIView):
    def get(self, request, keyword):

        movies = Movies.objects.all().filter(movie_name__contains=keyword)
        serialized = MovieSerializer(
            movies, many=True, context={"request": request})
        if serialized:

            return Response(serialized.data, status=status.HTTP_200_OK)

        return Response({"msg": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
