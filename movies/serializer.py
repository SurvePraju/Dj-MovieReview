from rest_framework import serializers
from .models import Movies, ReviewAndRate
from django.db.models import Avg


class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movies
        fields = ["movie_name", "movie_plot",
                  "movie_release", "average_rating"]

    def get_average_rating(self, obj):
        reviews_rating = ReviewAndRate.objects.filter(movie=obj)
        avg_rating = reviews_rating.aggregate(
            avg_rating=Avg('rating'))['avg_rating']
        if avg_rating:
            return round(avg_rating, 1)
        else:
            return None
