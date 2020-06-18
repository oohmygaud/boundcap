from django.shortcuts import render
from rest_framework import viewsets
from .models import Asset, Account
from .serializers import AssetSerializer, AccountSerializer

# Create your views here.
class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer