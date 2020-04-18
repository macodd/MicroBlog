from django import forms
from django.forms.utils import ErrorList


class FormUserNeededMixin(object):

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            form.errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in."])
            return self.form_invalid(form)


class UserOwnerMixin(object):

    def form_valid(self, form):
        if form.instance.user == self.request.user:
            return super().form_valid(form)
        else:
            form.errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User is not allowed to change content."])
        return self.form_invalid(form)