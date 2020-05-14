from django.views.generic import View, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render

from .forms import ContactForm

User = get_user_model()


class UserLoginView(LoginView):
    template_name = 'login.html'


class UserLogoutView(LogoutView):
    template_name = 'login.html'


class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q')
        qs = None
        if query:
            qs = User.objects.filter(
                username__icontains=query
            )
        context = {'users': qs}
        return render(request, 'search_view.html', context)


class TermsView(TemplateView):
    template_name = 'terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        previous_url = self.request.META['HTTP_REFERER']
        context['previous_url'] = previous_url
        return context


class ContactFormView(FormView):
    form_class      = ContactForm
    template_name   = 'contact.html'
    success_url     = '/contact/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        previous_url = self.request.META['HTTP_REFERER']
        context['previous_url'] = previous_url
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Mensaje enviado exitosamente!')
        return super().form_valid(form)

