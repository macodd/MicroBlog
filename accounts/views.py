from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import FormView
from django.views.generic import DetailView, View
from django.contrib.auth import get_user_model

from .forms import UserRegisterForm

from .models import UserProfile

User = get_user_model()


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'accounts/user_register.html'
    success_url = '/login/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email   = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password2')
        new_user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        new_user.set_password(password)
        new_user.save()
        return super().form_valid(form)


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
        UserProfile.objects.toggle_follow(request.user, toggle_user)
        return redirect("profiles:detail", username=username)
