from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.ubicaciones.forms import RegionComunaMixin

from .models import Perfil, Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["first_name", "last_name", "email"]
        labels = {"first_name": "Nombre", "last_name": "Apellido", "email": "Correo electrónico"}

class PerfilForm(RegionComunaMixin, forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["telefono", "comuna", "descripcion", "foto"]

