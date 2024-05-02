from django.test import TestCase
from .models import User, Appointment, Prescription, Payment
from django.utils import timezone

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', email='test@example.com', first_name='Test', last_name='User', address='123 Test St', date_of_birth=timezone.now().date(), role='patient')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'test_user')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.address, '123 Test St')
        self.assertEqual(self.user.date_of_birth, timezone.now().date())
        self.assertEqual(self.user.role, 'patient')

    def test_appointment_creation(self):
        appointment = Appointment.objects.create(patient=self.user, description='Sample appointment description', date=timezone.now().date())
        self.assertEqual(appointment.patient, self.user)
        self.assertEqual(appointment.description, 'Sample appointment description')
        self.assertEqual(appointment.date, timezone.now().date())

    def test_prescription_creation(self):
        appointment = Appointment.objects.create(patient=self.user, description='Sample appointment description', date=timezone.now().date())
        prescription = Prescription.objects.create(appointment=appointment, doctor=self.user, details='Sample prescription details', price=100)
        self.assertEqual(prescription.appointment, appointment)
        self.assertEqual(prescription.doctor, self.user)
        self.assertEqual(prescription.details, 'Sample prescription details')
        self.assertEqual(prescription.price, 100)

    def test_payment_creation(self):
        appointment = Appointment.objects.create(patient=self.user, description='Sample appointment description', date=timezone.now().date())
        prescription = Prescription.objects.create(appointment=appointment, doctor=self.user, details='Sample prescription details', price=100)
        payment = Payment.objects.create(prescription=prescription, payment_type='nhs', name_on_card='Test User', card_number='1234567890123456', cvv=123)
        self.assertEqual(payment.prescription, prescription)
        self.assertEqual(payment.payment_type, 'nhs')
        self.assertEqual(payment.name_on_card, 'Test User')
        self.assertEqual(payment.card_number, '1234567890123456')
        self.assertEqual(payment.cvv, 123)
