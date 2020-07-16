from django.contrib import admin
from .models import Asset, Account, Currency
# Register your models here.
admin.site.register(Asset)
admin.site.register(Account)
admin.site.register(Currency)