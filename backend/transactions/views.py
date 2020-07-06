from django.shortcuts import render
from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    filterset_fields = ["account", "category", "is_transfer", "is_spending", "merchant"]
    search_fields = ["account", "category", "merchant"]
    ordering_fields = "__all__"

    def get_queryset(self):
        qs = Transaction.objects.filter(
            account__entity__permissions__user=self.request.user
        ).order_by("import_date")
        return qs

    serializer_class = TransactionSerializer
