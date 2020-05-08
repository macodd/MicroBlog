from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import get_user_model
from django import forms
import re

User = get_user_model()


class RegisterForm(forms.Form):
    username        = forms.CharField(max_length=140, label='Nombre de Usuario')
    first_name      = forms.CharField(max_length=140, label='Nombre(s)')
    last_name       = forms.CharField(max_length=140, label='Apellido(s)')
    email           = forms.EmailField(widget=forms.EmailInput)
    accept_terms    = forms.BooleanField()
    password        = forms.CharField(widget=forms.PasswordInput)
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


class ContactForm(forms.Form):
    subject   = forms.CharField(label="Nombre Completo", max_length=140)
    email       = forms.EmailField(widget=forms.EmailInput)
    message     = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea,
        max_length=200
    )

    def clean(self):
        data = self.cleaned_data
        subject = data.get('subject')
        from_email = data.get('email')
        message = data.get('message')
        if subject and message and from_email:
            # try:
            #     send_mail(subject, message, from_email, ['codd82@gmail.com'])
            # except BadHeaderError:
            #     raise forms.ValidationError('Invalid header found.')
            return data
        else:
            raise forms.ValidationError('Todos los campos son requeridos.')