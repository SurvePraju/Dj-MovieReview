from django import forms
from .models import Movies, Genres, ReviewAndRate, People, Language


class AddMoviesForm(forms.ModelForm):

    class Meta:
        model = Movies
        fields = ["movie_name", "movie_cast", "movie_genre", "movie_plot", "movie_director", 'movie_writer',
                  "movie_length", "movie_release", "movie_budget", "movie_images", "movie_poster", "movie_language"]
        widgets = {
            "movie_name": forms.TextInput(attrs={"class": "form-control normal-text"}),
            "movie_plot": forms.Textarea(attrs={"class": "form-control"}),
            "movie_director": forms.TextInput(attrs={"class": "form-control normal-text"}),
            "movie_writer": forms.TextInput(attrs={"class": "form-control normal-text"}),
            "movie_length": forms.NumberInput(attrs={"class": "form-control"}),
            "movie_release": forms.DateInput(attrs={"class": "form-control normal-text", "placeholder": "YYYY-MM-DD"}),
            "movie_poster": forms.FileInput(attrs={"class": "form-control"}),
            "movie_images": forms.FileInput(attrs={"class": "form-control"}),
            "movie_language": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {"movie_images": "Movie Background (Landscape Format.)",
                  "movie_poster": "Movie Poster (Portrait Format.)"}


class ReviewAndRateForm(forms.ModelForm):
    class Meta:
        model = ReviewAndRate
        fields = ["review", "rating"]

        widgets = {
            "review": forms.Textarea(attrs={"class": "form-control"}),
            "rating": forms.Select(attrs={"class": "form-control", "style": "width: 50%;"})

        }


class AddGenresForm(forms.ModelForm):
    class Meta:
        model = Genres
        fields = ["genre_name", "genre_images"]
        labels = {
            "genre_name": "", "genre_images": ""
        }
        widgets = {
            "genre_name": forms.TextInput(attrs={"class": "form-control mb-3 normal-input", "placeholder": "Genre Name"}),
            "genre_images": forms.FileInput(attrs={"class": "form-control"})
        }


class AddActorsForm(forms.ModelForm):
    class Meta:
        model = People
        fields = ["actors_name", "actors_images"]
        labels = {
            "actors_name": "", "actors_images": ""
        }
        widgets = {
            "actors_name": forms.TextInput(attrs={"class": "form-control mb-3 normal-input", "placeholder": "Actors Name"}),
            "actors_images": forms.FileInput(attrs={"class": "form-control"})
        }
