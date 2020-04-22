from django.urls import path

from .views import TweetListAPIView, TweetCreateAPIView, RetweetAPIView

app_name = 'tweets'


urlpatterns = [
    path('', TweetListAPIView.as_view(), name='list'),  # /api/tweet/
    path('create/', TweetCreateAPIView.as_view(), name='create'),  # /api/tweet/create/
    path('<int:pk>/retweet/', RetweetAPIView.as_view(), name='retweet'),  # /api/tweet/pk/tweet

]
