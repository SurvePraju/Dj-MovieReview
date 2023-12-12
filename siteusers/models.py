from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    reviewer = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pic/")

    def __str__(self):
        return str(self.reviewer)
