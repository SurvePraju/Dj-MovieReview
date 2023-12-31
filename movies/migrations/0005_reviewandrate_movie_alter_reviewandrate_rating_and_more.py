# Generated by Django 4.2.2 on 2023-10-14 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0004_reviewandrate"),
    ]

    operations = [
        migrations.AddField(
            model_name="reviewandrate",
            name="movie",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="movies.movies",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="reviewandrate",
            name="rating",
            field=models.IntegerField(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1
            ),
        ),
        migrations.AlterField(
            model_name="reviewandrate",
            name="review",
            field=models.CharField(default=None, max_length=1000),
        ),
    ]
