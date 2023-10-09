from django import forms
from .models import Movies, Genres


class AddMoviesForm(forms.ModelForm):
    movie_genre = forms.ModelMultipleChoiceField(
        queryset=Genres.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        # required=False,
    )

    class Meta:
        model = Movies
        fields = ["movie_name", "movie_cast", "movie_genre", "movie_plot", "movie_director", 'movie_writer',
                  "movie_length", "movie_release", "movie_budget", "movie_images", "movie_poster", "movie_language"]
        widgets = {"movie_name": forms.TextInput(attrs={"class": "form-control"})
                   }
