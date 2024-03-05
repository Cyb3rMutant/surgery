from django.contrib import admin
from django.urls import path, include
from . import views
from .views import SignUpView

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", SignUpView.as_view(), name="signup"),
]
