from backend.transactions.models import Transaction
from backend.assets.models import Account
from backend.errors.models import Error
import traceback
import json
import re

def run():
    Transaction.objects.all().delete()
    with open("scripts/t.json") as f:
        data = json.load(f)
        import_transactions(data)

def import_transactions(data):
    for i in data:
        try:
            obj, _new = Transaction.objects.get_or_create(
                    external_id=i['id'],
                    account=Account.objects.get(title=i['account']),
                    defaults=dict(
                        category=i['category'],
                        amount_in_cents=int("".join(re.findall('\d+', i['amount']))),
                        is_transfer=i['isTransfer'],
                        is_spending=i['isSpending'],
                        merchant=i['merchant'],
                    )
                )
        except Account.DoesNotExist:
            Error.objects.create(title='transaction import error',
                description="Unable to find account '%s':\n%s"%(i['account'], i))