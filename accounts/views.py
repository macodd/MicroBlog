from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, View
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = UserProfile.objects.is_following(self.request.user, self.get_object())
        context['following'] = following
        return context


class UserFollowView(View):
    def get(self, request, username):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated:
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
        return redirect("profiles:detail", username=username)