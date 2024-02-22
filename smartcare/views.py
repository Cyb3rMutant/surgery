from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import PatientCreationForm


class SignUpView(CreateView):
    form_class = PatientCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
