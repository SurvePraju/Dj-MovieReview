from django.urls import path
from .views import *


urlpatterns = [
    path("add-movies/", AddMovies.as_view(), name="add_movies"),
    path("add-genre/", AddGenres.as_view(), name="add_genre"),
    path("add-actor/", Addactors.as_view(), name="add_actor"),

    path("movies-list/", MoviesPage.as_view(), name="movies"),
    path("movies-list-filtered/", FilterMovies.as_view(), name="filtered_movies"),
    path("movie-<str:id>/", SelectMovie.as_view(), name="selected_movie"),
    path("search/", Search.as_view(), name="search"),
    path("genres/", GenrePage.as_view(), name="genres"),
    path("add-watchlist/<int:movie_id>",
         AddWatchlist.as_view(), name="add_watchlist"),
    path("actors/", ActorsPage.as_view(), name="actors"),
    path("actor/<int:id>/", Actors.as_view(), name="selected_actor"),
    path("genres/<int:id>/", SelectedGenre.as_view(), name="selected_genre"),
    path("delete-genre/<int:id>/", delete_genre, name="delete_genre"),
    path("delete-actor/<int:id>/", delete_actor, name="delete_actor"),
    path("add-review/<int:id>/", Reviews.as_view(), name="add_review"),
]
