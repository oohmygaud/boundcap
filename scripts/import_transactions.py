from backend.transactions.models import Transaction, Category
from backend.assets.models import Account
from backend.errors.models import Error
import traceback
import json
import re

def run():
    Transaction.objects.all().delete()
    with open("scripts/t2.json") as f:
        data = json.load(f)
        import_transactions(data)

def import_transactions(data):
    for i in data:
        if len(Transaction.objects.filter(external_id=i['id'])) == 1:
            Transaction.objects.filter(external_id=i['id']).update(category=i['category'], externally_editted=True)
        else:
            try:
                category, _new = Category.objects.get_or_create(title=i['category'])
                obj, _new = Transaction.objects.get_or_create(
                        external_id=i['id'],
                        account=Account.objects.get(title=i['account']),
                        defaults=dict(
                            category=category,
                            amount_in_cents=int("".join(re.findall('\d+', i['amount']))),
                            is_transfer=i['isTransfer'],
                            is_spending=i['isSpending'],
                            merchant=i['merchant'],
                        )
                    )
            except Account.DoesNotExist:
                Error.objects.create(title='transaction import error',
                    description="Unable to find account '%s':\n%s"%(i['account'], i))