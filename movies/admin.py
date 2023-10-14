from django.contrib import admin
from .models import *
# Register your models here.

# @admin.register(Movies)
# class RegisterMovies(admin.ModelAdmin):

admin.site.register(Movies)
admin.site.register(Language)
admin.site.register(People)
admin.site.register(Genres)


@admin.register(WatchList)
class AdminWatchList(admin.ModelAdmin):
    list_display = ["user", "movies"]


@admin.register(ReviewAndRate)
class AdminReviewAndRate(admin.ModelAdmin):
    list_display = ["viewer", "movie", "review", "rating"]
