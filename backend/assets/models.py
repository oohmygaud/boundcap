from django.db import models
from backend.users.models import Entity
import uuid
# Create your models here.
def cutePk():
    return str(uuid.uuid4())[-8:]

class CutePKBase(models.Model):
    id = models.CharField(max_length=8, primary_key=True, default=cutePk, editable=False)

    class Meta:
        abstract = True

class Currency(models.Model):
    abbreviation = models.CharField(max_length=8)

class Asset(CutePKBase):
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True, blank=True)

class Account(Asset):
    externalId = models.PositiveIntegerField()
    title = models.CharField(max_length=128)
    STATUS_CHOICES = [("active", "active"), ("closed", "closed")]
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="active")
    current_balance_in_cents = models.IntegerField()
