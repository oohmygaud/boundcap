from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import permissions

# Create your models here.
class Entity(models.Model):
    title = models.CharField(max_length=128)

class User(AbstractUser):
    pass
