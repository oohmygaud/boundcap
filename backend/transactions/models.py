from django.db import models
from backend.assets.models import Account
import uuid
# Create your models here.
class RandomPKBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Transaction(RandomPKBase):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    import_date = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=36)
    amount_in_cents = models.IntegerField()
    is_transfer = models.BooleanField()
    is_spending = models.BooleanField()
    merchant = models.CharField(max_length=120)
    internally_editted = models.BooleanField(default=False)
    externally_editted = models.BooleanField(default=False)
    json_blob = models.TextField(null=True, blank=True)
