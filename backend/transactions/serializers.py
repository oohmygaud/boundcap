from rest_framework import serializers
from .models import Transaction
from backend.assets.serializers import AccountSerializer


class TransactionSerializer(serializers.ModelSerializer):
    account_data = serializers.SerializerMethodField()

    def get_account_data(self, obj):
        return AccountSerializer(obj.account).data

    class Meta:
        model = Transaction
        fields = [
            "id",
            "external_id",
            "account",
            "account_data",
            "import_date",
            "effective_date",
            "category",
            "amount_in_cents",
            "merchant",
            "is_transfer",
            "is_spending"
        ]

