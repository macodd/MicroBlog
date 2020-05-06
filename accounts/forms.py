from django.contrib.auth import get_user_model
from django import forms

from .models import UserProfile

User = get_user_model()


class UserRegisterForm(forms.Form):
    username        = forms.CharField(max_length=140, label='Nombre de Usuario')
    first_name      = forms.CharField(max_length=140, label='Nombre(s)')
    last_name       = forms.CharField(max_length=140, label='Apellido(s)')
    email           = forms.EmailField()
    accept_terms    = forms.BooleanField()
    password        = forms.CharField(widget=forms.PasswordInput)
    password2       = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Contraseñas deben coincidir")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Nombre de usuario ya existe')
        return username

    def clean_accept_terms(self):
        accepted = self.cleaned_data.get('accept_terms')
        if not accepted:
            raise forms.ValidationError('Para registrarse debe acceder a los terminos y condiciones')
        return accepted


class UserUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = self.request.user.first_name
        self.fields['last_name'].widget.attrs['placeholder'] = self.request.user.last_name
        self.fields['email'].widget.attrs['placeholder'] = self.request.user.email

    first_name  = forms.CharField(max_length=40, required=False)
    last_name   = forms.CharField(max_length=40, required=False)
    image       = forms.ImageField(allow_empty_file=True, required=False)
    email       = forms.EmailField(required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(email)
        return email

    def clean(self):
        data = self.cleaned_data
        f_name  = data.get('first_name')
        l_name  = data.get('last_name')
        img     = data.get('image')
        email = data.get('email')
        u = self.request.user
        user_prof = UserProfile.objects.get(user__username=u)
        if f_name != '':
            user_prof.user.first_name = f_name.title()
        if l_name != '':
            user_prof.user.last_name = l_name.title()
        if email != '':
            user_prof.user.email = email
        if img is not None:
            user_prof.image = img

        user_prof.save()

        return data
