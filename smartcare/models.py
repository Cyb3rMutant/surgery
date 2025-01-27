from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.
# Create your models here.
class User(AbstractUser):
    ROLES = (
        ("patient", "Patient"),
        ("doctor", "Doctor"),
    )
    role = models.CharField(max_length=20, choices=ROLES, default="patient")
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)  # Change to DateField


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField()
    price = models.IntegerField()


class Payment(models.Model):
    PAYMENT_TYPE = (
        ("nhs", "NHS"),
        ("private", "Private"),
    )
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE, default="nhs")
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    name_on_card = models.CharField(max_length=48)
    card_number = models.CharField(max_length=16)
    cvv = models.IntegerField()
