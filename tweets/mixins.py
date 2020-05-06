from django import forms
from django.forms.utils import ErrorList


class FormUserNeededMixin(object):

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            form.errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["Usuario debe tener una sesion iniciada."])
            return self.form_invalid(form)


class UserOwnerMixin(object):

    def form_valid(self, form):
        if form.instance.user == self.request.user:
            return super().form_valid(form)
        else:
            form.errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["Solo el creador puede cambiar el contenido."])
        return self.form_invalid(form)