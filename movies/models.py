from django.db import models

# Create your models here.


class Genre(models.Model):
    genre_category = models.CharField(max_length=50, unique=True, blank=False)


class People(models.Model):
    person_name = models.CharField(max_length=100, blank=False)


class Movies(models.Model):
    movie_name = models.CharField(max_length=100, unique=True, blank=False)
    movie_poster = models.ImageField(upload_to="poster/")
    movie_images = models.ImageField(upload_to="movie_images/")
    movie_plot = models.TextField(max_length=1000)
    movie_length = models.SmallIntegerField(max_length=3)
    movie_release = models.DateField()
    movie_budget = models.PositiveIntegerField()
