from backend.transactions.models import Transaction
from backend.assets.models import Account
import traceback
import json
import re

def run():
    Transaction.objects.all().delete()
    with open("scripts/t.json") as f:
        data = json.load(f)
        for i in data:
            Transaction.objects.create(
                account=Account.objects.get(title=i['account']),
                category=i['category'],
                amount_in_cents=int("".join(re.findall('\d+', i['amount']))),
                is_transfer=i['isTransfer'],
                is_spending=i['isSpending'],
                merchant=i['merchant'],
            )