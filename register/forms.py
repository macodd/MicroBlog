from django.contrib.auth import get_user_model
from django import forms
import re

User = get_user_model()


class RegisterForm(forms.Form):
    username        = forms.CharField(max_length=140, label='Nombre de Usuario', help_text='Mínimo 4 caracteres')
    first_name      = forms.CharField(max_length=140, label='Nombre(s)')
    last_name       = forms.CharField(max_length=140, label='Apellido(s)')
    email           = forms.EmailField(widget=forms.EmailInput)
    accept_terms    = forms.BooleanField(label='Acceptar Terminos')
    password        = forms.CharField(label='Contraseña', widget=forms.PasswordInput, help_text='Mínimo 8 caracteres')
    password2       = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Nombre de usuario ya existe')
        if len(username) < 4:
            raise forms.ValidationError('Nombre de usuario debe ser minimo 4 caracteres')
        if not re.match(r'[A-Za-z0-9_-]+$', username):
            raise forms.ValidationError("Nombre de usuario solo puede tener letras, numeros, _ o -")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Contraseña debe ser mínimo de 8 caracteres')
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Contraseñas deben coincidir")
        return password2
