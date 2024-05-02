from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from .models import Appointment, Payment, Prescription, User


class PatientSignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(
        label="Date of Birth",  # Label for the field
        widget=forms.SelectDateWidget(
            years=range(1900, timezone.now().year + 1)
        ),  # Calendar widget
        required=False,  # Field not required
    )

    alias_choices = (
        ("", "Select Alias"),  # Default empty value
        ("Dr.", "Dr."),
        ("Mr.", "Mr."),
        (
            "Miss.",
            "Miss.",
        ),
        ("Mrs", "Mrs."),
        ("Prof", "Prof."),
    )
    alias = forms.ChoiceField(choices=alias_choices, label="Alias")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "alias",  # Added alias here
            "first_name",
            "last_name",
            "address",
            "date_of_birth",  # Added date_of_birth here
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLES[0][0]
        user.date_of_birth = self.cleaned_data["date_of_birth"]  # Save date of birth
        if commit:
            user.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(
        label="Date of Birth",  # Label for the field
        widget=forms.SelectDateWidget(
            years=range(1900, timezone.now().year + 1)
        ),  # Calendar widget
        required=False,  # Field not required
    )

    alias_choices = (
        ("", "Select Alias"),  # Default empty value
        ("Dr.", "Dr."),
        ("Mr.", "Mr."),
        (
            "Miss.",
            "Miss.",
        ),
        ("Mrs", "Mrs."),
        ("Prof", "Prof."),
    )
    alias = forms.ChoiceField(choices=alias_choices, label="Alias")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "alias",  # Added alias here
            "first_name",
            "last_name",
            "address",
            "date_of_birth",  # Added date_of_birth here
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLES[1][0]
        user.date_of_birth = self.cleaned_data["date_of_birth"]  # Save date of birth
        user.is_active = False
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("is_active",)


class PersonalDetailsForm(UserChangeForm):
    date_of_birth = forms.DateField(
        label="Date of Birth",  # Label for the field
        widget=forms.SelectDateWidget(
            years=range(1900, timezone.now().year + 1)
        ),  # Calendar widget
        required=False,  # Field not required
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "date_of_birth",  # Add date_of_birth here
        )


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=["%m/%d/%Y", "%m/%d/%y"],
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
