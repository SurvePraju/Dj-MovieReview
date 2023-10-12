from django.urls import path
from .views import *


urlpatterns = [
    path("add-movies/", AddMovies.as_view(), name="add_movies"),
    path("movies-list/", MoviesPage.as_view(), name="movies"),
    path("movie-<str:id>/", SelectMovie.as_view(), name="selected_movie"),
    path("genres/", GenrePage.as_view(), name="genres"),
    path("add-watchlist/<int:movie_id>",
         AddWatchlist.as_view(), name="add_watchlist"),
    path("actors/", ActorsPage.as_view(), name="actors"),
    path("actor/<int:id>/", Actors.as_view(), name="selected_actor"),
    path("genres/<int:id>/", SelectedGenre.as_view(), name="selected_genre"),
]
