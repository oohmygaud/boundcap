from backend.transactions.models import Category
import traceback
import json
import re

def run():
    with open("scripts/transactionCategories.json") as f:
        data = json.load(f)
        import_categories(data)


def import_categories(data):
    for i in data:
        obj, _new = Category.objects.get_or_create(title=i)
