from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class PatientSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLES[0][0]
        if commit:
            user.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLES[1][0]
        user.is_active = False
        if commit:
            user.save()
        return user


class NurseSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLES[2][0]
        user.is_active = False
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("is_active",)
