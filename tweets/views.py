from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

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


class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated:
            new_tweet = Tweet.objects.retweet(request.user, tweet)
            return redirect('home')
        return HttpResponseRedirect(tweet.get_absolute_url())


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
    model = Tweet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy('tweet:create')
        return context
