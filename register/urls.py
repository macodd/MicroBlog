from django.urls import path

from .views import (
    RegisterView,
    ThanksForRegistering,
    UserChangePassword,
    UserChangePasswordDone,
    UserPasswordReset,
    UserPasswordResetDone,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView
)

app_name = 'register'

urlpatterns = [
    path('', RegisterView.as_view(), name='start'),
    path('done/', ThanksForRegistering.as_view(), name='done'),
    path('password-change/', UserChangePassword.as_view(), name='password_change'),
    path('password-change/done/', UserChangePasswordDone.as_view(), name='password_change_done'),
    path('reset/', UserPasswordReset.as_view(), name='password_reset'),
    path('reset/done/', UserPasswordResetDone.as_view(), name='password_reset_done'),
    path('reset-confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-confirm/complete/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]