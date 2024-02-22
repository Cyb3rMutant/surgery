from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Patient


class PatientCreationForm(UserCreationForm):

    class Meta:
        model = Patient
        fields = ("username", "email")


class PatientChangeForm(UserChangeForm):

    class Meta:
        model = Patient
        fields = ("username", "email")
