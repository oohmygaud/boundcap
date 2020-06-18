from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "import_date",
            "effective_date",
            "category",
            "amount_in_cents",
            "merchant",
        ]

