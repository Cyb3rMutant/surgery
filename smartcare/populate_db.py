from .models import User, Appointment, Prescription, Payment
from django.utils import timezone
from random import choice, randint
from datetime import timedelta


def populate_database():
    # Create users
    patients = []
    doctors = []
    for i in range(10):
        patient = User.objects.create_user(
            username=f"patient{i}", password="password", role="patient"
        )
        doctor = User.objects.create_user(
            username=f"doctor{i}", password="password", role="doctor"
        )
        patients.append(patient)
        doctors.append(doctor)

    # Create appointments, prescriptions, and payments
    today = timezone.now()
    for _ in range(100):
        patient = choice(patients)
        doctor = choice(doctors)
        appointment_date = today - timedelta(days=randint(0, 365))
        appointment = Appointment.objects.create(
            patient=patient, description="Sample Description", date=appointment_date
        )
        prescription = Prescription.objects.create(
            appointment=appointment,
            doctor=doctor,
            details="Sample Prescription Details",
            price=randint(50, 200),
        )
        payment_type = choice(["nhs", "private"])
        Payment.objects.create(
            payment_type=payment_type,
            prescription=prescription,
            name_on_card=f"{patient.first_name} {patient.last_name}",
            card_number="1234567812345678",
            cvv=123,
        )

    print("Database populated successfully!")
