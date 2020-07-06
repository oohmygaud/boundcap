from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
from ..users.models import User, Entity, UserAllowedEntity
from ..assets.models import Currency, Account
from .views import TransactionViewSet
from .models import Transaction

# Create your tests here.
transactionView = TransactionViewSet.as_view(
    {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
)


class TranscationTestCase(TestCase):
    def test_create_update_delete_transaction_api(self):
        factory = APIRequestFactory()
        # Create a user
        user = User.objects.create_user(
            username="testUser", email="example@example.com", password="somepassword123"
        )
        # Create an entity
        entity = Entity.objects.create(title="TestEntity")
        # Create a currency
        currency = Currency.objects.create(abbreviation="USD")
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity, user=user)
        # Create an account
        account = Account.objects.create(
            id=1,
            externalId=1234567,
            title="TestAccount",
            current_balance_in_cents=1234,
            entity=entity,
            currency=currency,
        )
        self.assertEqual(Account.objects.count(), 1)
        # Post to transaction API
        request = factory.post(
            "/transactions/",
            {
                "account": account.id,
                "category": "Test",
                "amount_in_cents": 1234,
                "is_transfer": False,
                "is_spending": True,
                "merchant": "Testaurant",
            },
        )
        force_authenticate(request, user=user)
        transactionView(request)
        # Get list of transactions
        request = factory.get("/transactions/")
        force_authenticate(request, user=user)
        response = transactionView(request)
        # Confirm one transaction was created
        self.assertEqual(Transaction.objects.count(), 1)

        transaction = Transaction.objects.first()
        # Update the transaction's category
        request2 = factory.put(
            "/transactions/" + str(transaction.id),
            {
                "account": account.id,
                "category": "Tester",
                "amount_in_cents": 1234,
                "is_transfer": False,
                "is_spending": True,
                "merchant": "Testaurant",
            },
        )
        force_authenticate(request2, user=user)
        response2 = transactionView(request2, pk=transaction.id)
        # Confirm there is still one transaction with the corrected category
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.first().category, "Tester")
        # Delete the transaction
        request3 = factory.delete("/transactions/" + str(transaction.id))
        force_authenticate(request3, user=user)
        response3 = transactionView(request3, pk=transaction.id)
        # Confirm there are zero transactions
        self.assertEqual(Transaction.objects.count(), 0)

    def test_list_transactions_for_entities(self):
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
        # Create a currency
        currency = Currency.objects.create(abbreviation="USD")
        # Create permissions for each entity and user
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity1, user=user1)
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity2, user=user2)
        # Create an account for entity1
        account1 = Account.objects.create(
            id=1,
            externalId=1234567,
            title="TestAccount1",
            current_balance_in_cents=1234,
            entity=entity1,
            currency=currency,
        )
        # Confirm account is made
        self.assertEqual(Account.objects.count(), 1)
        # User1 posts to transaction API
        request1 = factory.post(
            "/transactions/",
            {
                "account": account1.id,
                "category": "Test",
                "amount_in_cents": 1234,
                "is_transfer": False,
                "is_spending": True,
                "merchant": "Testaurant",
            },
        )
        force_authenticate(request1, user=user1)
        transactionView(request1)
        # Create an account for entity2
        account2 = Account.objects.create(
            id=2,
            externalId=1234567,
            title="TestAccount1",
            current_balance_in_cents=1234,
            entity=entity2,
            currency=currency,
        )
        # Confirm there are two accounts total
        self.assertEqual(Account.objects.count(), 2)
        # User2 posts to transaction API
        request2 = factory.post(
            "/transactions/",
            {
                "account": account2.id,
                "category": "Test",
                "amount_in_cents": 5678,
                "is_transfer": False,
                "is_spending": True,
                "merchant": "Testaurant",
            },
        )
        force_authenticate(request2, user=user2)
        transactionView(request2)
        # User1 gets the list of transactions
        request3 = factory.get("/transactions/")
        force_authenticate(request3, user=user1)
        response = transactionView(request3)
        # Confirm the results are only user1's transactions
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["amount_in_cents"], 1234)

    def test_transaction_pagination(self):
        factory = APIRequestFactory()
        # Create a user
        user = User.objects.create_user(
            username="testUser", email="example@example.com", password="somepassword123"
        )
        # Create an entity
        entity = Entity.objects.create(title="TestEntity")
        # Create a currency
        currency = Currency.objects.create(abbreviation="USD")
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity, user=user)
        # Create an account
        account = Account.objects.create(
            id=1,
            externalId=1234567,
            title="TestAccount",
            current_balance_in_cents=1234,
            entity=entity,
            currency=currency,
        )
        self.assertEqual(Account.objects.count(), 1)
        # Create three transactions
        create_transaction1 = {
            "account": account.id,
            "category": "Test",
            "amount_in_cents": 1234,
            "is_transfer": False,
            "is_spending": True,
            "merchant": "Testaurant",
        }
        create_transaction2 = {
            "account": account.id,
            "category": "Test",
            "amount_in_cents": 5678,
            "is_transfer": False,
            "is_spending": True,
            "merchant": "Testaurant",
        }
        create_transaction3 = {
            "account": account.id,
            "category": "Test",
            "amount_in_cents": 9012,
            "is_transfer": False,
            "is_spending": True,
            "merchant": "Testaurant",
        }
        # Post to transaction API
        request1 = factory.post("/transactions/", create_transaction1)
        force_authenticate(request1, user=user)
        transactionView(request1)
        request2 = factory.post("/transactions/", create_transaction2)
        force_authenticate(request2, user=user)
        transactionView(request2)
        request3 = factory.post("/transactions/", create_transaction3)
        force_authenticate(request3, user=user)
        transactionView(request3)

        self.assertEqual(Transaction.objects.count(), 3)

        request4 = factory.get("/transactions/?limit=2")
        force_authenticate(request4, user=user)
        response1 = transactionView(request4)
        self.assertEqual(len(response1.data['results']), 2)

        request5 = factory.get("/transactions/?offset=2")
        force_authenticate(request5, user=user)
        response2 = transactionView(request5)
        self.assertEqual(len(response2.data['results']), 1)
        self.assertEqual(response2.data['results'][0]['amount_in_cents'], 9012)

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
        userAllowedEntity = UserAllowedEntity.objects.create(entity=entity, user=user)
        # Create an account
        account = Account.objects.create(
            id=1,
            externalId=1234567,
            title="TestAccount",
            current_balance_in_cents=1234,
            entity=entity,
            currency=currency,
        )
        self.assertEqual(Account.objects.count(), 1)
        # Create two transactions
        create_transaction1 = {
            "account": account.id,
            "category": "Food",
            "amount_in_cents": 5678,
            "is_transfer": False,
            "is_spending": True,
            "merchant": "Testaurant",
        }
        create_transaction2 = {
            "account": account.id,
            "category": "Gym",
            "amount_in_cents": 1234,
            "is_transfer": True,
            "is_spending": False,
            "merchant": "Yoga",
        }
        # Post to transaction API
        request1 = factory.post("/transactions/", create_transaction1)
        force_authenticate(request1, user=user)
        transactionView(request1)
        request2 = factory.post("/transactions/", create_transaction2)
        force_authenticate(request2, user=user)
        transactionView(request2)

        request3 = factory.get('/transactions/?category=Food')
        force_authenticate(request3, user=user)
        response1 = transactionView(request3)
        self.assertEqual(len(response1.data['results']), 1)

        request4 = factory.get('/transactions/?category=Gym')
        force_authenticate(request4, user=user)
        response2 = transactionView(request4)
        self.assertEqual(len(response2.data['results']), 1)

        request5 = factory.get('/transactions?search=Yoga')
        force_authenticate(request5, user=user)
        response3 = transactionView(request5)
        self.assertEqual(len(response3.data['results']), 1)
        self.assertEqual(response3.data['results'][0]["category"], "Gym")
        

