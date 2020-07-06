from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import User, Entity, UserAllowedEntity
from .serializers import UserSerializer, EntitySerializer, UserAllowedEntitySerializer


def private(request):
    if request.user.is_authenticated:
        return render(request, "base.html")
    else:
        return redirect("/login/")

def public(request):
    if not request.user.is_authenticated:
        return render(request, "base.html")
    else:
        return redirect("/")

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer

class UserAllowedEntityViewSet(viewsets.ModelViewSet):
    queryset = UserAllowedEntity.objects.all()
    serializer_class = UserAllowedEntitySerializer

    def get_queryset(self):
        qs = UserAllowedEntity.objects.filter(user=self.request.user)
        return qs

