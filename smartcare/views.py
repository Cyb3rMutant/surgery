from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AppointmentForm, PrescriptionForm, UserCreationForm
from django.views.generic import ListView, TemplateView
from django.db import transaction
from django.contrib import messages

from .models import Appointment, Prescription, User
from .forms import DoctorSignUpForm, NurseSignUpForm, PatientSignUpForm


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


def logout_view(request):
    logout(request)
    return redirect("home")


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


class MakeAppointment(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "patient/appointment.html"

    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.patient = self.request.user
        appointment.save()
        messages.success(
            self.request,
            "appointment booked",
        )
        return redirect("home")


class AppointmentListView(ListView):
    model = Appointment
    ordering = ("date",)
    context_object_name = "appointments"
    template_name = "doctor/view-appointments.html"

    def get_queryset(self):
        queryset = Appointment.objects.all()
        return queryset


def appoint(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if Prescription.objects.filter(pk=pk).exists():
        print("already done")
        return redirect("home")

    if request.method == "POST":
        form = PrescriptionForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                prescription = form.save(commit=False)
                prescription.appointment = appointment
                prescription.doctor = request.user
                prescription.save()

                print("now done")
                return redirect("home")
    form = PrescriptionForm()

    return render(
        request,
        "doctor/appoint.html",
        {
            "appointment": appointment,
            "form": form,
        },
    )


class ViewPrescriptions(ListView):
    model = Prescription
    ordering = ("date",)
    context_object_name = "prescriptions"
    template_name = "patient/view-prescriptions.html"

    def get_queryset(self):
        appointments = Appointment.objects.filter(patient=self.request.user)
        print("\n\n\n", appointments)
        queryset = Prescription.objects.filter(appointment__in=appointments)
        return queryset
