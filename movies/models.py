from django.db import models
from django.contrib.auth.models import User
from .youtubeapi import search_videos
# Create your models here.


class Genres(models.Model):
    genre_name = models.CharField(max_length=50, unique=True, blank=False)
    genre_images = models.ImageField(upload_to="genre_images/")

    def __str__(self) -> str:
        return self.genre_name


class People(models.Model):
    actors_name = models.CharField(max_length=100, blank=False)
    actors_images = models.ImageField(upload_to="actors_images/")

    def __str__(self) -> str:
        return self.actors_name


class Language(models.Model):
    language = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self) -> str:
        return self.language


class Movies(models.Model):
    movie_name = models.CharField(max_length=100, unique=True, blank=False)
    movie_poster = models.ImageField(upload_to="poster/")
    movie_images = models.ImageField(upload_to="movie_images/")
    movie_plot = models.TextField(max_length=1000)
    movie_length = models.SmallIntegerField()
    movie_release = models.DateField()
    movie_director = models.CharField(max_length=100)
    movie_writer = models.CharField(max_length=190)
    movie_budget = models.PositiveIntegerField()
    movie_genre = models.ManyToManyField(Genres)
    movie_cast = models.ManyToManyField(People)
    movie_language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.movie_name

    def release_year(self):
        return self.movie_release.strftime("%Y")

    def movie_budget_string(self):

        return format(self.movie_budget, ",")

    def movie_genre_string(self):
        genres = "/ ".join([movie.genre_name for movie in self.movie_genre.all()])
        return genres

    def movie_cast_string(self):
        casts = ", ".join([name.actors_name for name in self.movie_cast.all()])
        return casts

    def youtube_search(self):
        video_id = search_videos(self.movie_name)
        return f"https://www.youtube.com/embed/{video_id}?rel=0"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ForeignKey(Movies, on_delete=models.CASCADE)


class ReviewAndRate(models.Model):
    rating_choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000, default=None)
    rating = models.IntegerField(choices=rating_choices, default=1)

    def __str__(self):
        return f"{self.id}"

    def return_list(self):
        return [i for i in range(self.rating)]

    def length(self):
        return [i for i in range(5)]
