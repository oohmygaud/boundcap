from django.contrib import admin
from backend.transactions.models import Transaction, Category
# Register your models here.
admin.site.register(Transaction)
admin.site.register(Category)