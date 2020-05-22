from django.urls import path

from tweets.api.views import TweetListAPIView

from .views import UserProfileAPIView, UsernameTakenAPIView

app_name = 'accounts'

urlpatterns = [
    path('<str:username>/', UserProfileAPIView.as_view(), name='user-profile'),
    path('<str:username>/tweet/', TweetListAPIView.as_view(), name='user-tweets'),
    path('find/<str:username>/', UsernameTakenAPIView.as_view(), name='find-user')
]
