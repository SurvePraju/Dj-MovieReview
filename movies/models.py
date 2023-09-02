from django.db import models

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


class Movies(models.Model):
    movie_name = models.CharField(max_length=100, unique=True, blank=False)
    movie_poster = models.ImageField(upload_to="poster/")
    movie_images = models.ImageField(upload_to="movie_images/")
    movie_plot = models.TextField(max_length=1000)
    movie_length = models.SmallIntegerField()
    movie_release = models.DateField()
    movie_budget = models.PositiveIntegerField()
    movie_genre = models.ManyToManyField(Genres)
    movie_cast = models.ManyToManyField(People)

    def __str__(self) -> str:
        return self.movie_name
