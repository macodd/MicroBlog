from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(forms.Form):
    username    = forms.CharField()
    first_name  = forms.CharField(max_length=80)
    last_name   = forms.CharField(max_length=80)
    email       = forms.EmailField()
    password    = forms.CharField(widget=forms.PasswordInput)
    password2   = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
