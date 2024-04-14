from django.contrib import admin
from django.urls import path, include
from . import views
from .views import (
    AppointmentListView,
    PaymentsPerMonth,
    SignUpView,
    MakeAppointment,
    ViewPrescriptions,
    appoint,
    logout_view,
    pay,
)

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("logout", logout_view, name="logout"),
    path("make-appointment", MakeAppointment.as_view(), name="make-appointment"),
    path("view-appointments", AppointmentListView.as_view(), name="view-appointments"),
    path("view-prescriptions", ViewPrescriptions.as_view(), name="view-prescriptions"),
    path("view-payments", PaymentsPerMonth.as_view(), name="view-payments"),
    path("appoint/<int:pk>/", appoint, name="appoint"),
    path("pay/<int:pk>/", pay, name="pay"),
]
