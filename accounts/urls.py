from django.urls import path

from .views import UserDetailView, UserFollowView, user_update_view

app_name = 'accounts'

urlpatterns = [
    path('<slug:username>/edit/', user_update_view, name='edit'),
    path('<slug:username>/', UserDetailView.as_view(), name='detail'),
    path('<slug:username>/follow/', UserFollowView.as_view(), name='follow'),
]