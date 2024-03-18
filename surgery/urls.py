"""
URL configuration for surgery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic.base import TemplateView
from smartcare import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("", include("smartcare.urls")),
    path("", include("django.contrib.auth.urls")),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "accounts/signup/doctor/",
        views.DoctorSignUpView.as_view(),
        name="doctor_signup",
    ),
    path(
        "accounts/signup/nurse/",
        views.NurseSignUpView.as_view(),
        name="nurse_signup",
    ),
    path(
        "accounts/signup/patient/",
        views.PatientSignUpView.as_view(),
        name="patient_signup",
    ),
]
