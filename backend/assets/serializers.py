from rest_framework import serializers
from .models import Asset, Account


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = [
            "id",
            "currency",
            "entity",
            "created_at",
            "added_at",
            "updated_at",
            "archived_at",
        ]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["externalId", "title", "status", "current_balance_in_cents"]
