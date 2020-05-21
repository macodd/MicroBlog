from django.views.generic import TemplateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from .forms import RegisterForm
from .tasks import change_password_confirmation_mail


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register/register.html'
    success_url = '/register/done/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email   = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password2')
        new_user = User.objects.create_user(
            username=username,
            first_name=first_name.title(),
            last_name=last_name.title(),
            email=email
        )
        new_user.set_password(password)
        new_user.save()
        return super().form_valid(form)


class ThanksForRegistering(TemplateView):
    template_name = 'register/register-done.html'


class UserChangePassword(PasswordChangeView):
    template_name = 'register/password_change_form.html'
    success_url = '/register/password-change/done/'

    def form_valid(self, form):
        user = self.request.user
        user_obj = User.objects.get(user)
        change_password_confirmation_mail.delay(user_obj.email)
        return super().form_valid(form)


class UserChangePasswordDone(PasswordChangeDoneView):
    template_name = 'register/password_change_done.html'


class UserPasswordReset(PasswordResetView):
    template_name = 'register/password_reset_form.html'
    success_url = '/register/reset/done/'
    email_template_name = 'register/password_reset_email.html'


class UserPasswordResetDone(PasswordResetDoneView):
    template_name = 'register/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'register/password_reset_confirm.html'
    success_url = '/register/reset-confirm/complete/'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'register/password_reset_complete.html'
