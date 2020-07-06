from django.test import TestCase
from .models import User


class UserTest(TestCase):
    def test_create_user(self):
        test_user = User.objects.create_user(
            username="banana21", email="example@example.com", password="somepassword123"
        )

        self.assertEqual(len(User.objects.all()), 1)
