from django.db import models

# Create your models here.


class Genre(models.Model):
    genre_category = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self) -> str:
        return self.genre_category


class People(models.Model):
    actors_name = models.CharField(max_length=100, blank=False)

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

    def __str__(self) -> str:
        return self.movie_name


class Reviews(models.Model):
    review = models.TextField(max_length=1000)
    # rate=models
    pass
