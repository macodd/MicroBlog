from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render

from .models import HashTag


class HashTagView(LoginRequiredMixin, View):
    def get(self, request, hashtag, **kwargs):
        obj, created = HashTag.objects.get_or_create(tag=hashtag)
        return render(request, 'hashtags/tag_view.html', {'obj': obj})