# Generated by Django 4.2.2 on 2023-09-03 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="movies",
            name="movie_director",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="movies",
            name="movie_writer",
            field=models.CharField(default=2, max_length=190),
            preserve_default=False,
        ),
    ]