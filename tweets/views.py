from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin


class TweetCreateView(FormUserNeededMixin, CreateView):
    template_name   = 'tweets/create_view.html'
    model           = Tweet
    form_class      = TweetModelForm


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    template_name   = 'tweets/update_view.html'
    model           = Tweet
    form_class      = TweetModelForm


class TweetDeleteView(DeleteView):
    template_name   = 'tweets/delete_view.html'
    model           = Tweet
    success_url     = reverse_lazy('tweet:list')


class TweetDetailView(DetailView):
    template_name   = 'tweets/detail_view.html'
    model           = Tweet


class TweetListView(ListView):
    template_name   = 'tweets/list_view.html'
    model           = Tweet

    def get_queryset(self):
        qs = Tweet.objects.all()
        query = self.request.GET.get('q', None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy('tweet:create')
        return context
