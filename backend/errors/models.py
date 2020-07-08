from django.db import models

# Create your models here.
class Error(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)