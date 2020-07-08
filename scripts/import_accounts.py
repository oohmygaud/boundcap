from backend.assets.models import Account, Currency
from backend.users.models import Entity
import yaml

def run():
    currency, created = Currency.objects.get_or_create(abbreviation='USD')
    entity, created = Entity.objects.get_or_create(title='Lee Personal')
    
    with open("scripts/accounts.yaml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        import_accounts(data, currency, entity)

def import_accounts(data, currency, entity):
    for i in data:
        account, created = Account.objects.update_or_create(
            externalId=i['accountId'],
            title=i['accountName'],
            current_balance_in_cents=i['currentBalance'],
            currency_id=currency.id,
            entity_id=entity.id,
            defaults={'current_balance_in_cents': i['currentBalance']}
        )