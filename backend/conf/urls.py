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
from django.conf.urls import include
from backend.assets.views import AssetViewSet, AccountViewSet
from backend.transactions.views import TransactionViewSet
from backend.users.views import UserViewSet
from rest_framework import routers
from backend.users import views

router = routers.SimpleRouter()
router.register(r"assets", AssetViewSet)
router.register(r"accounts", AccountViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"users", UserViewSet)

api_urlpatterns = [path("auth/", include("rest_registration.api.urls"))] + router.urls

urlpatterns = [
    path("api/", include(api_urlpatterns)),
    path("admin/", admin.site.urls),
    path("", views.private),
    path("register/", views.public),
    path("login/", views.public),
]
