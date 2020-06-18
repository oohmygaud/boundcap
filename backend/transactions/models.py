from django.db import models
from assets.models import Account

# Create your models here.
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    import_date = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateTimeField()
    category = models.CharField(max_length=36)
    amount_in_cents = models.IntegerField()
    is_transfer = models.BooleanField()
    is_spending = models.BooleanField()
    merchant = models.CharField(max_length=120)
    internally_editted = models.BooleanField()
    externally_editted = models.BooleanField()
    json_blob = models.TextField()
