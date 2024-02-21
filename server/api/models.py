from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=1000)

class ModelRefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=1000)