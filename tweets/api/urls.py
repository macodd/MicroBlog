from django.urls import path

from .views import TweetListAPIView, TweetCreateAPIView

app_name = 'tweets'


urlpatterns = [
    path('', TweetListAPIView.as_view(), name='list'),
    path('create/', TweetCreateAPIView.as_view(), name='create')
]
