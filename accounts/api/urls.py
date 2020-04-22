from django.urls import path

from tweets.api.views import TweetListAPIView

app_name = 'accounts'

urlpatterns = [
    path('<str:username>/tweet/', TweetListAPIView.as_view(), name='user-tweets')
]