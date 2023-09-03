from django.urls import path
from .views import *


urlpatterns = [
    path("add-movies/", AddMovies.as_view(), name="add_movies"),
    path("movies-list/", MoviesPage.as_view(), name="movies"),
    path("movie/<int:id>/",
         SelectMovie.as_view(), name="selected_movie"),
    path("genre/", GenrePage.as_view(), name="genres"),
]
