from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Appointment, Prescription, Payment
from .forms import AppointmentForm, PaymentForm, PrescriptionForm, PersonalDetailsForm

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_authenticated_patient(self):
        user = User.objects.create_user(username="test_patient", password="password", role="patient")
        self.client.login(username="test_patient", password="password")

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboards/patient.html")

    def test_logout_view(self):
        user = User.objects.create_user(username="test_user", password="password")
        self.client.login(username="test_user", password="password")

        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirects after logout

    def test_patient_signup_view(self):
        response = self.client.get(reverse("patient-signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_doctor_signup_view(self):
        response = self.client.get(reverse("doctor-signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_update_details_view(self):
        user = User.objects.create_user(username="test_user", password="password")
        self.client.login(username="test_user", password="password")

        response = self.client.get(reverse("update-details"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update.html")

    def test_make_appointment_view_post(self):
        user = User.objects.create_user(username="test_patient", password="password", role="patient")
        self.client.login(username="test_patient", password="password")

        response = self.client.post(reverse("make-appointment"), {"description": "Sample appointment description"})

        self.assertTrue(Appointment.objects.exists())
        self.assertRedirects(response, reverse("home"))

    def test_appoint_view(self):
        user = User.objects.create_user(username="test_doctor", password="password", role="doctor")
        self.client.login(username="test_doctor", password="password")
        appointment = Appointment.objects.create(patient=User.objects.create_user(username="patient", password="password", role="patient"),
                                                  description="Test Appointment", date=timezone.now().date())

        response = self.client.get(reverse("appoint", args=[appointment.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "doctor/appoint.html")

    def test_view_prescriptions_view(self):
        user = User.objects.create_user(username="test_patient", password="password", role="patient")
        self.client.login(username="test_patient", password="password")
        appointment = Appointment.objects.create(patient=user, description="Test Appointment", date=timezone.now().date())
        prescription = Prescription.objects.create(appointment=appointment, doctor=user, details="Test Prescription", price=100)

        response = self.client.get(reverse("view-prescriptions"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient/view-prescriptions.html")

    def test_pay_view(self):
        user = User.objects.create_user(username="test_patient", password="password", role="patient")
        self.client.login(username="test_patient", password="password")
        appointment = Appointment.objects.create(patient=user, description="Test Appointment", date=timezone.now().date())
        prescription = Prescription.objects.create(appointment=appointment, doctor=user, details="Test Prescription", price=100)

        response = self.client.get(reverse("pay", args=[prescription.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient/pay.html")

    def test_payments_per_month_view(self):
        user = User.objects.create_user(username="test_doctor", password="password", role="doctor")
        self.client.login(username="test_doctor", password="password")
        appointment = Appointment.objects.create(patient=User.objects.create_user(username="patient", password="password", role="patient"),
                                                  description="Test Appointment", date=timezone.now().date())
        prescription = Prescription.objects.create(appointment=appointment, doctor=user, details="Test Prescription", price=100)
        payment = Payment.objects.create(prescription=prescription, payment_type='nhs', name_on_card='Test User', card_number='1234567890123456', cvv=123)

        response = self.client.get(reverse("payments-per-month"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "doctor/view-payments.html")
