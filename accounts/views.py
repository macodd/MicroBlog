from django.views.generic import DetailView
from django.contrib.auth import get_user_model

User = get_user_model()


class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    model = User

