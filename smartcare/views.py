from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AppointmentForm, PaymentForm, PrescriptionForm, PersonalDetailsForm
from django.views.generic import ListView, TemplateView
from django.db import transaction
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from django.db.models.functions import TruncMonth
from .decorators import doctor_required, patient_required


from .models import Appointment, Payment, Prescription, User
from .forms import DoctorSignUpForm, PatientSignUpForm


def home(request):
    if request.user.is_authenticated:
        match request.user.role:
            case "patient":
                return render(request, "dashboards/patient.html")
            case "doctor":
                if request.user.is_active:
                    return render(request, "dashboards/doctor.html")
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


# @method_decorator([login_required], name="dispatch")
# class UpdateDetails(UpdateView):
#     model = User
#     form_class = PersonalDetailsForm
#     template_name = "update.html"
#
#     def form_valid(self, form):
#         u = form.save(commit=False)
#         u.save()
#         messages.success(
#             self.request,
#             "details updated",
#         )
#         return redirect("home")


@login_required
def updateDetails(request):
    if request.method == "POST":
        form = PersonalDetailsForm(data=request.POST, instance=request.user)
        update = form.save(commit=False)
        update.user = request.user
        update.save()
    else:
        form = PersonalDetailsForm(instance=request.user)

    return render(request, "update.html", {"form": form})


@method_decorator([login_required, patient_required], name="dispatch")
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


@method_decorator([login_required, doctor_required], name="dispatch")
class AppointmentListView(ListView):
    model = Appointment
    ordering = ("date",)
    context_object_name = "appointments"
    template_name = "doctor/view-appointments.html"

    def get_queryset(self):
        queryset = Appointment.objects.all()
        return queryset


@login_required
@doctor_required
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


@method_decorator([login_required, patient_required], name="dispatch")
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


@login_required
@doctor_required
def pay(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if Payment.objects.filter(pk=pk).exists():
        print("already done")
        return redirect("home")

    if request.method == "POST":
        form = PaymentForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                payment = form.save(commit=False)
                payment.prescription = prescription
                payment.save()

                print("now done")
                return redirect("home")
    form = PaymentForm()

    return render(
        request,
        "patient/pay.html",
        {
            "prescription": prescription,
            "form": form,
        },
    )


@method_decorator([login_required, doctor_required], name="dispatch")
class PaymentsPerMonth(ListView):
    template_name = "doctor/view-payments.html"
    context_object_name = "monthly_payments"

    def get_queryset(self):
        # Calculate the start date and end date for the last 10 months
        today = timezone.now()
        ten_months_ago = today - timedelta(days=10 * 30)  # Assuming 30 days per month
        end_date = today.replace(day=1)  # First day of the current month
        start_date = ten_months_ago.replace(day=1)  # First day of the 10th month ago

        # Aggregate payments for each month
        monthly_payments = (
            Payment.objects.filter(
                payment_type="nhs",
                prescription__appointment__date__gte=start_date,
                prescription__appointment__date__lt=end_date,
            )
            .annotate(month=TruncMonth("prescription__appointment__date"))
            .values("month")
            .annotate(total_payment=Sum("prescription__price"))
            .order_by("-month")
        )  # Get the last 10 months
        from pprint import pprint

        pprint([x for x in monthly_payments])

        return monthly_payments
