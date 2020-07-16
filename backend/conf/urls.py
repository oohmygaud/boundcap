"""boundcap_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, re_path
from backend.assets.views import AssetViewSet, AccountViewSet, CurrencyViewSet
from backend.transactions.views import TransactionViewSet, CategoryViewSet
from backend.errors.views import ErrorViewSet
from backend.users.views import UserViewSet, EntityViewSet, UserAllowedEntityViewSet
from rest_framework import routers
from backend.users import views

router = routers.SimpleRouter()
router.register(r"assets", AssetViewSet)
router.register(r"accounts", AccountViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"users", UserViewSet)
router.register(r"errors", ErrorViewSet)
router.register(r"currencies", CurrencyViewSet)
router.register(r"entities", EntityViewSet)
router.register(r"user_permissions", UserAllowedEntityViewSet)
router.register(r"categories", CategoryViewSet)

api_urlpatterns = [path("auth/", include("rest_registration.api.urls"))] + router.urls

urlpatterns = [
    path("api/", include(api_urlpatterns)),
    path("admin/", admin.site.urls),
    path("", views.private),
    path("register/", views.public),
    path("login/", views.public),
    path("entities/", views.private),
    re_path(r"^entities/.*", views.private),
    re_path(r"^user_permissions/.*", views.private),
    re_path(r"^transactions/.*", views.private)
]
