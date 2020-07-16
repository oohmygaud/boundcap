from rest_framework import serializers
from .models import Asset, Account, Currency

ASSET_FIELDS =  [
            "id",
            "currency",
            "entity",
            "created_at",
            "added_at",
            "updated_at",
            "archived_at",
        ]

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ASSET_FIELDS


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["externalId", "title", "status", "current_balance_in_cents"] + ASSET_FIELDS

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["abbreviation"]