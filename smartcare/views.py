from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render
from .forms import UserCreationForm
from django.views.generic import TemplateView

from .models import User
from .forms import DoctorSignUpForm, NurseSignUpForm, PatientSignUpForm


class SignUpView(TemplateView):
    template_name = "registration/signup.html"


class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "patient"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class NurseSignUpView(CreateView):
    model = User
    form_class = NurseSignUpForm
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "nurse"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "doctor"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


def home(request):
    if request.user.is_authenticated:
        match request.user.role:
            case "patient":
                return render(request, "dashboards/patient.html")
            case "doctor":
                if request.user.is_active:
                    return render(request, "dashboards/doctor.html")
            case "nurse":
                if request.user.is_active:
                    return render(request, "dashboards/nurse.html")
    return render(request, "home.html")
