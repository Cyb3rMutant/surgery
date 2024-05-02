from django.test import TestCase
from .forms import PatientSignUpForm, DoctorSignUpForm, AppointmentForm, PrescriptionForm, PaymentForm
from django.utils import timezone

class TestForms(TestCase):
    def test_patient_signup_form_valid_data(self):
        form = PatientSignUpForm(data={
            'username': 'test_user',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'address': '123 Test St',
            'date_of_birth': timezone.now().date(),
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_doctor_signup_form_valid_data(self):
        form = DoctorSignUpForm(data={
            'username': 'test_doctor',
            'email': 'doctor@example.com',
            'first_name': 'Doctor',
            'last_name': 'Test',
            'address': '456 Doctor St',
            'date_of_birth': timezone.now().date(),
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_appointment_form_valid_data(self):
        form = AppointmentForm(data={
            'description': 'Sample appointment description',
            'date': timezone.now().date(),
        })
        self.assertTrue(form.is_valid())

    def test_prescription_form_valid_data(self):
        form = PrescriptionForm(data={
            'details': 'Sample prescription details',
            'price': 100,
        })
        self.assertTrue(form.is_valid())

    def test_payment_form_valid_data(self):
        form = PaymentForm(data={
            'payment_type': 'nhs',
            'name_on_card': 'Test User',
            'card_number': '1234567890123456',
            'cvv': 123,
        })
        self.assertTrue(form.is_valid())
