from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import DetailView, View, FormView
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import UserRegisterForm, UserUpdateForm

from .models import UserProfile

User = get_user_model()


class FollowingView(LoginRequiredMixin, DetailView):
    template_name   = 'accounts/following.html'
    slug_url_kwarg  = 'username'
    slug_field      = 'username'
    model           = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = UserProfile.objects.is_following(self.request.user, self.get_object())
        context['following'] = following
        return context


class FollowerView(LoginRequiredMixin, DetailView):
    template_name   = 'accounts/followers.html'
    slug_url_kwarg  = 'username'
    slug_field      = 'username'
    model           = User


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
            first_name=first_name.title(),
            last_name=last_name.title(),
            email=email
        )
        new_user.set_password(password)
        new_user.save()
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name   = 'accounts/user_detail.html'
    slug_url_kwarg  = 'username'
    slug_field      = 'username'
    model           = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = UserProfile.objects.is_following(self.request.user, self.get_object())
        context['following'] = following
        return context


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, username):
        toggle_user = get_object_or_404(User, username__iexact=username)
        UserProfile.objects.toggle_follow(request.user, toggle_user)
        return redirect("profiles:detail", username=username)


def user_update_view(request, *args, **kwargs):
    username = kwargs.get('username')
    if request.user.username != username:
        messages.add_message(request, messages.ERROR, 'No tiene permitido acceso')
        return redirect('profiles:detail', username=request.user.username)
    template = 'accounts/user_update.html'
    user = UserProfile.objects.get(user__username=username)
    form = UserUpdateForm(request.POST or None, request.FILES or None, request=request)
    context = {
        'user_img': user.image,
        'form': form
    }
    try:
        if form.is_valid():
            return redirect('profiles:detail', username=username)
    except OSError:
        return redirect('profiles:detail', username=username)
    except AttributeError:
        return redirect('profiles:detail', username=username)
    return render(request, template, context)
