from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    ROLES = (("patient", "Patient"), ("doctor", "Doctor"), ("nurse", "Nurse"))
    role = models.CharField(max_length=20, choices=ROLES, default="patient")


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
