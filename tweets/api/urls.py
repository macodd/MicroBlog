from django.urls import path

from .views import TweetListAPIView

app_name = 'tweets'


urlpatterns = [
    path('', TweetListAPIView.as_view(), name='list'),
]
