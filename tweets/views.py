from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin


class RetweetView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        Tweet.objects.retweet(request.user, tweet)
        return redirect('home')


class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
    template_name   = 'tweets/create_view.html'
    model           = Tweet
    form_class      = TweetModelForm


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    template_name   = 'tweets/update_view.html'
    model           = Tweet
    form_class      = TweetModelForm


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    template_name   = 'tweets/delete_view.html'
    model           = Tweet
    success_url     = reverse_lazy('tweet:list')


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name   = 'tweets/detail_view.html'
    model           = Tweet


class TweetListView(LoginRequiredMixin, ListView):
    template_name   = 'tweets/list_view.html'
    model = Tweet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy('tweet:create')
        return context
