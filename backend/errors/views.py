from django.shortcuts import render
from .models import Error
from .serializers import ErrorSerializer
from rest_framework import viewsets
# Create your views here.
class ErrorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer