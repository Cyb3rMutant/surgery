from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import PatientCreationForm, PatientChangeForm
from .models import Patient


class PatientAdmin(UserAdmin):
    add_form = PatientCreationForm
    form = PatientChangeForm
    model = Patient
    list_display = [
        "email",
        "username",
    ]


admin.site.register(Patient, PatientAdmin)
