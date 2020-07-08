from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
from ..users.models import User, Entity, UserAllowedEntity
from ..errors.models import Error
from .models import Currency, Account
from .views import AccountViewSet
import yaml
from scripts.import_accounts import import_accounts

# Create your tests here.
accountView = AccountViewSet.as_view(
    {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
)

def get_account_data():
    account_data = yaml.load(open("backend/assets/fixtures/testAccount.yaml"), Loader=yaml.FullLoader)
    return account_data


class AssetTestCase(TestCase):
    def test_create_update_delete_account_api(self):
        factory = APIRequestFactory()
        # Create a user
        user = User.objects.create_user(
            username="testUser", email="example@example.com", password="somepassword123"
        )
        # Create an entity
        entity = Entity.objects.create(title="TestEntity")
        # Create a currency
        currency = Currency.objects.create(abbreviation="USD")
        # Create permissions for the entity
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity, user=user)
        # Post to the account API
        create_account = {
            "externalId": 1234567,
            "title": "TestAccount",
            "current_balance_in_cents": 1234,
            "entity": entity.id,
            "currency": currency.id,
        }
        request = factory.post("/accounts/", create_account)
        force_authenticate(request, user=user)
        accountView(request)
        # Get the list of accounts
        request = factory.get("/accounts/")
        force_authenticate(request, user=user)
        response = accountView(request)
        # Confirm one account was created
        self.assertEqual(Account.objects.count(), 1)

        account = Account.objects.first()
        # Update the current balance of the account
        request2 = factory.put(
            "/accounts/" + account.id,
            {
                "externalId": 1234567,
                "title": "TestAccount",
                "current_balance_in_cents": 5678,
                "entity": entity.id,
                "currency": currency.id,
            },
        )
        force_authenticate(request2, user=user)
        response2 = accountView(request2, pk=account.id)
        # Confirm there is still one account with the corrected balance
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.first().current_balance_in_cents, 5678)
        # Delete the account
        request3 = factory.delete("/accounts/" + account.id)
        force_authenticate(request3, user=user)
        response3 = accountView(request3, pk=account.id)
        # Confirm there are zero accounts
        self.assertEqual(Account.objects.count(), 0)

    def test_user_allowed_entities(self):
        factory = APIRequestFactory()
        # Create user 1
        user1 = User.objects.create_user(
            username="testUser1",
            email="example@example.com",
            password="somepassword123",
        )
        # Create user 2
        user2 = User.objects.create_user(
            username="testUser2",
            email="example@example.com",
            password="somepassword123",
        )
        # Create entity 1
        entity1 = Entity.objects.create(title="TestEntity1")
        # Create entity 2
        entity2 = Entity.objects.create(title="TestEntity2")
        # User 1 has permissions for Entity 1 (Personal Entity)
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity1, user=user1)
        # User 1 has permissions for 2 (Group Entity)
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity2, user=user1)
        # User 2 has permissions for Entity 2 (Group Entity)
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity2, user=user2)

        # Create a currency
        currency = Currency.objects.create(abbreviation="USD")
        # Post to the account API
        create_account = {
            "externalId": 1234567,
            "title": "TestAccount",
            "current_balance_in_cents": 1234,
            "entity": entity1.id,
            "currency": currency.id,
        }
        request = factory.post("/accounts/", create_account)
        force_authenticate(request, user=user1)
        response = accountView(request)

        false_user = factory.get("/accounts/")
        force_authenticate(false_user, user=user2)
        response = accountView(false_user)
        # User 2 has no accounts
        self.assertEqual(len(response.data["results"]), 0)

    def test_account_pagination(self):
        factory = APIRequestFactory()
        # Create a user
        user = User.objects.create_user(
            username="testUser", email="example@example.com", password="somepassword123"
        )
        # Create an entity
        entity = Entity.objects.create(title="TestEntity")
        # Create a currency
        currency = Currency.objects.create(abbreviation="USD")
        # Create permissions for the entity
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity, user=user)
        # Create three accounts
        create_account1 = {
            "externalId": 1111111,
            "title": "TestAccount1",
            "current_balance_in_cents": 1111,
            "entity": entity.id,
            "currency": currency.id,
        }
        create_account2 = {
            "externalId": 2222222,
            "title": "TestAccount2",
            "current_balance_in_cents": 2222,
            "entity": entity.id,
            "currency": currency.id,
        }
        create_account3 = {
            "externalId": 3333333,
            "title": "TestAccount3",
            "current_balance_in_cents": 3333,
            "entity": entity.id,
            "currency": currency.id,
        }
        request1 = factory.post("/accounts/", create_account1)
        force_authenticate(request1, user=user)
        response1 = accountView(request1)
        request2 = factory.post("/accounts/", create_account2)
        force_authenticate(request2, user=user)
        response2 = accountView(request2)
        request3 = factory.post("/accounts/", create_account3)
        force_authenticate(request3, user=user)
        response3 = accountView(request3)
        # Confirm three accounts made
        self.assertEqual(Account.objects.count(), 3)
        # Get a limit of 2 account results
        request4 = factory.get("/accounts/?limit=2")
        force_authenticate(request4, user=user)
        response4 = accountView(request4)
        # Confirm data returns two accounts
        self.assertEqual(len(response4.data["results"]), 2)
        # Get accounts with an offset of 2
        request5 = factory.get("/accounts/?offset=2")
        force_authenticate(request5, user=user)
        response5 = accountView(request5)
        # Confirm there is one account (starting at two, there is one account after)
        self.assertEqual(len(response5.data["results"]), 1)
        self.assertEqual(response5.data["results"][0]["title"], "TestAccount3")

    def test_django_filters(self):
        factory = APIRequestFactory()
        # Create a user
        user = User.objects.create_user(
            username="testUser", email="example@example.com", password="somepassword123"
        )
        # Create an entity
        entity = Entity.objects.create(title="TestEntity")
        # Create a currency
        currency = Currency.objects.create(abbreviation="USD")
        # Create permissions for the entity
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity, user=user)
        # Create two accounts
        create_account1 = {
            "externalId": 1111111,
            "title": "TestAccount1",
            "current_balance_in_cents": 2222,
            "entity": entity.id,
            "currency": currency.id,
        }
        create_account2 = {
            "externalId": 2222222,
            "title": "TestAccount2",
            "current_balance_in_cents": 1111,
            "entity": entity.id,
            "currency": currency.id,
            "status": "closed"
        }
        request1 = factory.post("/accounts/", create_account1)
        force_authenticate(request1, user=user)
        response1 = accountView(request1)
        request2 = factory.post("/accounts/", create_account2)
        force_authenticate(request2, user=user)
        response2 = accountView(request2)
        # Get accounts whose status is active
        request3 = factory.get('/accounts/?status=active')
        force_authenticate(request3, user=user)
        response3 = accountView(request3)
        # Confirm one account is active
        self.assertEqual(len(response3.data["results"]), 1)
        # Get accounts whose status is closed
        request4 = factory.get('/accounts/?status=closed')
        force_authenticate(request4, user=user)
        response4 = accountView(request4)
        # Confirm one account is closed
        self.assertEqual(len(response4.data["results"]), 1)
        # Get all users searching for 2 in the title
        request5 = factory.get('/accounts?search=2')
        force_authenticate(request5, user=user)
        response5 = accountView(request5)
        # Confirm results are one account with the title TestAccount2
        self.assertEqual(len(response5.data["results"]), 1)
        self.assertEqual(response5.data["results"][0]["title"], "TestAccount2")
        # Get accounts in order of current_balance_in_cents
        request6 = factory.get('/accounts?ordering=current_balance_in_cents')
        force_authenticate(request6, user=user)
        response6 = accountView(request6)
        # Confirm first result is the account with the least amount, with externalId 2222222
        self.assertEqual(response6.data["results"][0]["externalId"], 2222222)
    
    def test_import_account(self):
        factory = APIRequestFactory()
        # Create a user
        user = User.objects.create_user(
            username="testUser", email="example@example.com", password="somepassword123"
        )
        # Create an entity
        entity = Entity.objects.create(title="TestEntity")
        # Create a currency
        currency = Currency.objects.create(abbreviation="USD")
        # Create permissions for the entity
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity, user=user)
        # Import account
        import_accounts(get_account_data(), currency, entity)
        # Confirm one account was imported
        self.assertEqual(Account.objects.count(), 1)
