from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Appointment, Payment, Prescription, User


class PatientSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLES[0][0]
        if commit:
            user.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLES[1][0]
        user.is_active = False
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("is_active",)


class PersonalDetailsForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
        )


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=["%d/%m/%Y", "%d/%m/%y"],
        widget=forms.SelectDateWidget(),
        initial=timezone.now().date(),
    )

    class Meta:
        model = Appointment
        fields = (
            "description",
            "date",
        )


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = (
            "details",
            "price",
        )


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = (
            "payment_type",
            "name_on_card",
            "card_number",
            "cvv",
        )
