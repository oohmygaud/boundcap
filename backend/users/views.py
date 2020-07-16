from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Entity, UserAllowedEntity
from .serializers import UserSerializer, EntitySerializer, UserAllowedEntitySerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django import forms

@csrf_exempt
def private(request):
    if request.user.is_authenticated:
        return render(request, "base.html")
    else:
        return redirect("/login/")

@csrf_exempt
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

    def get_queryset(self):
        qs = Entity.objects.filter(permissions__user=self.request.user).distinct()
        return qs

class UserAllowedEntityViewSet(viewsets.ModelViewSet):
    queryset = UserAllowedEntity.objects.all()
    serializer_class = UserAllowedEntitySerializer

    def get_queryset(self):
        entities = Entity.objects.filter(permissions__user=self.request.user)
        qs = UserAllowedEntity.objects.filter(entity__in=entities)
        return qs

    @action(detail=False, methods=['post'])
    def allow_user_by_email(self, request):
        print(request)
        user = User.objects.filter(email=request.data.get('email')).first()
        entity = Entity.objects.filter(pk=request.data.get('entity'), permissions__user=self.request.user).first()
        if not user or not entity:
            return Response({'error': 'invalid user or entity'}, status=status.HTTP_401_UNAUTHORIZED)

        permission = UserAllowedEntity.objects.create(user=user, entity=entity)
        return Response({
            'ok': True,
            'data': UserAllowedEntitySerializer(permission).data
        })
