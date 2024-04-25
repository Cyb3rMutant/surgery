from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Appointment, Prescription, Payment

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_authenticated_patient(self):
        user = User.objects.create_user(username="test_patient", password="password", role="patient")
        self.client.login(username="test_patient", password="password")

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "dashboards/patient.html")


    def test_make_appointment_view_post(self):
        user = User.objects.create_user(username="test_patient", password="password", role="patient")
        self.client.login(username="test_patient", password="password")

        response = self.client.post(reverse("make-appointment"), {"description": "Sample appointment description"})

        self.assertTrue(Appointment.objects.exists())

        self.assertRedirects(response, reverse("home"))


