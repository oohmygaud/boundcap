from rest_framework import serializers
from .models import Transaction, Category
from backend.assets.serializers import AccountSerializer


class TransactionSerializer(serializers.ModelSerializer):
    account_data = serializers.SerializerMethodField()
    category_title = serializers.SerializerMethodField()


    def get_account_data(self, obj):
        return AccountSerializer(obj.account).data

    def get_category_title(self, obj):
        return obj.category.title

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
            "category_title",
            "amount_in_cents",
            "merchant",
            "is_transfer",
            "is_spending",
            "internally_editted",
            "externally_editted",
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]