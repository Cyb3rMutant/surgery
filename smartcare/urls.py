from django.contrib import admin
from django.urls import path, include
from . import views
from .views import SignUpView, MakeAppointment

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("make-appointment", MakeAppointment.as_view(), name="make-appointment"),
]
