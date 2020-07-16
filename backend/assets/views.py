from django.shortcuts import render
from rest_framework import viewsets
from .models import Asset, Account, Currency
from .serializers import AssetSerializer, AccountSerializer, CurrencySerializer

# Create your views here.
class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filterset_fields = ["title", "status"]
    search_fields = ["title"]
    ordering_fields = '__all__'

    def get_queryset(self):
        qs = Account.objects.filter(entity__permissions__user=self.request.user)
        return qs

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer