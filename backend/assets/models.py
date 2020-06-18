from django.db import models
from users.models import Entity

# Create your models here.
class Currency(models.Model):
    abbreviation = models.CharField(max_length=8)

class Asset(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    archived_at = models.DateTimeField()

class Account(Asset):
    externalId = models.PositiveIntegerField()
    title = models.CharField(max_length=128)
    STATUS_CHOICES = [("active", "active"), ("closed", "closed")]
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="active")
    current_balance_in_cents = models.IntegerField()
